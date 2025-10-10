import os
import hashlib
import re
import requests
from typing import List, Dict
from PyPDF2 import PdfReader

PERPLEXITY_API_KEY = "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"

SAMPLE_TEXT = "Artificial Intelligence (AI) involves creating intelligent agents capable of reasoning, learning, and adapting. Key topics include search algorithms, machine learning, natural language processing, and robotics. Ethical implications of AI and societal impacts are important considerations."



# --- Utility functions ---
def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("-\n", "").replace("\n", " ")).strip()

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print("⚠️ PDF read error:", e)
    return text.strip()

def get_pdf_hash(pdf_path: str) -> str:
    h = hashlib.sha256()
    with open(pdf_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# --- AI Text Sanitizer ---
def sanitize_ai_text(q: str) -> str:
    q = re.sub(r"^#+.*", "", q, flags=re.MULTILINE)
    q = re.sub(r"[*_`>~-]+", "", q)
    q = re.sub(r"(?i)^ *(here|generate|list|create|write|provide|give).*?:", "", q, flags=re.MULTILINE)
    q = re.sub(r"(?i)(source|explanation|answer|key|based on).*?:.*", "", q)
    q = re.sub(r"(?i)with the missing word.*", "", q)
    q = re.sub(r"(?i)correct answer.*", "", q)
    q = re.sub(r"\n{2,}", "\n", q)
    q = re.sub(r"\s{2,}", " ", q)
    return q.strip()

# --- Perplexity API question generator ---
def generate_questions_from_text(context: str, qtype: str, n: int) -> List[str]:
    system_msg = "You are an expert teacher creating exam questions."
    
    if qtype == "MCQ":
        prompt = f"""
    Generate {n} high-quality multiple-choice questions from the following text.
    - Use specific terms from the text in questions and answers.
    - Each question must have four options (A-D) and the correct answer clearly labeled as 'Answer: B'.
    - Number questions 1., 2., 3., etc.
    - Do NOT include explanations or additional text.

    Text:
    {context}
    """
    elif qtype == "FIB":
        prompt = f"""
        Generate {n} fill-in-the-blank questions from the text below.
        - Select a key word or phrase from the text to hide as a blank: '_____'.
        - Provide the missing word immediately after the question as 'Answer: <word>'.
        - Number questions 1., 2., 3., etc.
        - Do NOT add explanations or extra text.

    Text:
    {context}
    """
    else:  # Short / Long questions
        prompt = f"""
        Generate {n} {qtype.lower()} questions from the following text.
        - Use specific content from the text.
        - Number questions 1., 2., 3., etc.
        - Do NOT include answers or explanations.
        """

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {PERPLEXITY_API_KEY}", "Content-Type": "application/json"},
            json={"model": "sonar", "messages":[{"role":"system","content":system_msg},{"role":"user","content":prompt}],
                  "temperature":0.7, "max_tokens":1000},
            timeout=30
        )
        data = response.json()
        if "choices" not in data:
            print("⚠️ Perplexity API raw response:", data)
            return []
        questions_text = data["choices"][0]["message"]["content"].strip()
        questions = re.split(r"\n(?=\d+\.)", questions_text)  # split by numbered questions
        return [sanitize_ai_text(q) for q in questions if q.strip()][:n]
    except Exception as e:
        print("⚠️ Perplexity API error:", e)
        return []

# --- MCQ Parser ---
def parse_mcq(q_text: str) -> Dict:
    q_text = sanitize_ai_text(q_text)
    opts = re.findall(r"[A-D][\.\)]\s*(.+?)(?=\n[A-D][\.\)]|$)", q_text)
    opts = list(dict.fromkeys([sanitize_ai_text(o) for o in opts]))[:4]
    stem = re.split(r"[A-D][\.\)]", q_text)[0].strip()
    ans_match = re.search(r"Answer\s*[:\-]?\s*([A-D])", q_text, re.IGNORECASE)
    answer = opts[ord(ans_match.group(1).upper()) - 65] if ans_match else None
    return {"stem": stem, "options": opts, "answer": answer}

def generate_mcqs(text: str, n: int) -> List[Dict]:
    raw = generate_questions_from_text(text, "MCQ", n)
    return [parse_mcq(q) for q in raw]

def generate_fibs(text: str, n: int) -> List[Dict]:
    raw = generate_questions_from_text(text, "FIB", n)
    fibs = []

    for q in raw:
        # Try to find the answer from "Answer: ..." pattern
        ans_match = re.search(r"Answer:\s*(.+)", q)
        answer = ans_match.group(1).strip() if ans_match else None

        # Remove "Answer: ..." from question text
        stem = re.sub(r"Answer:\s*.+", "", q).strip()

        # Replace answer with blank if we found it, else just add blank at end
        if answer and answer in stem:
            stem = stem.replace(answer, "_____")
        else:
            # If answer not found in text, just append a blank at the end
            if not stem.endswith("."):
                stem += " "
            stem += "_____"

        fibs.append({"stem": stem, "answer": answer})

    return fibs

def generate_short_questions(text: str, n: int) -> List[str]:
    return generate_questions_from_text(text, "Short", n)

def generate_long_questions(text: str, n: int) -> list:
    """
    Generate n long questions from structured text.
    Filters out headings, section numbers, and other non-content lines.
    Produces clean questions asking for reasoning and examples.
    """
    if not text or len(text.split()) < 50:
        text += " This text provides detailed information suitable for generating analytical and applied long questions."

    # Split text into candidate sentences by '.', ':', or newline
    candidates = re.split(r'(?<=[.:])\s+|\n', text)
    candidates = [s.strip() for s in candidates if s.strip()]

    questions = []
    count = 0

    for s in candidates:
        # Skip short fragments
        if len(s.split()) < 5:
            continue
        # Skip headings / all uppercase or number-heavy lines
        if s.isupper() or re.match(r'^[A-Z0-9\s\-\.:]+$', s):
            continue
        # Skip lines with weird spacing or incomplete words (like "t o AI")
        if re.search(r'\b[a-zA-Z]\s+[a-zA-Z]\b', s):
            continue
        # Skip lines that are clearly quotations or citations only
        if re.match(r'^“.*”$', s):
            s = s.strip('“”')  # Keep content inside quotes

        # Remove repetitive phrase if present
        s = re.sub(r"(?i)^Discuss the implications of the following idea: ?", "", s).strip()

        # Form the question
        question = f"{s} Explain your reasoning and provide examples or applications where relevant."
        questions.append(question)
        count += 1
        if count >= n:
            break

    # If not enough questions, repeat some with slight variation
    while len(questions) < n:
        for s in candidates:
            if len(s.split()) < 5:
                continue
            if s.isupper() or re.match(r'^[A-Z0-9\s\-\.:]+$', s):
                continue
            s = re.sub(r"(?i)^Discuss the implications of the following idea: ?", "", s).strip()
            question = f"{s} Explain how this concept can be applied or interpreted in practice."
            questions.append(question)
            if len(questions) >= n:
                break

    return questions[:n]
# --- Full Question Paper ---
def generate_question_paper(text: str = None, pdf_path: str = None, subject: str = "General",
                            counts: Dict[str,int] = None) -> dict:
    counts = counts or {"mcq":10, "fib":10, "short":5, "long":4}
    if pdf_path and os.path.isfile(pdf_path):
        text = extract_text_from_pdf(pdf_path)
        hash_hex = get_pdf_hash(pdf_path)
    else:
        text = text or SAMPLE_TEXT
        hash_hex = hashlib.sha256(text.encode()).hexdigest()
    text = clean_text(text)

    return {
        "subject": subject,
        "hash": hash_hex,
        "questions_by_level": {
            "MCQ": generate_mcqs(text, counts["mcq"]),
            "FillBlanks": generate_fibs(text, counts["fib"]),
            "Short": generate_short_questions(text, counts["short"]),
            "Long": generate_long_questions(text, counts["long"]),
        }
    }
