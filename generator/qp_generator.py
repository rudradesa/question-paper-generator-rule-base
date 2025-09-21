import os
import hashlib
import re
import random
import requests
from typing import List, Dict
from PyPDF2 import PdfReader


PERPLEXITY_API_KEY = ""

def clean_text(text: str) -> str:
    text = text.replace("-\n", "").replace("\n", " ")
    return re.sub(r"\s+", " ", text).strip()

def sentences(text: str) -> List[str]:
    return re.split(r'(?<=[.!?]) +', text)

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


def perplexity_generate_questions_batch(context: str, qtype="MCQ", n=5) -> List[str]:
    """
    Generate `n` questions at once for a given text context.
    Returns a list of strings (each question + options as returned by Perplexity).
    """
    system_msg = "You are a teacher generating exam questions from text."

    if qtype == "MCQ":
        user_msg = f"""
Generate {n} multiple-choice questions from the following text.
For each question, provide four options labeled A-D, and mark the correct answer like: 'Answer: B'.

Text:
{context}
"""
    elif qtype == "FIB":
        user_msg = f"""
Generate {n} fill-in-the-blank questions from the following text.
Replace the blank word with '_____'. Provide the answer at the end like: 'Answer: <word>'.

Text:
{context}
"""
    else:
        user_msg = f"Generate {n} {qtype.lower()} questions from the following text:\n{context}"

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "sonar", 
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                "temperature": 0.7,
                "max_tokens": 600  
            },
            timeout=30
        )
        data = response.json()
        if "choices" not in data:
            print("⚠️ Perplexity API raw response:", data)
            return []

        questions_text = data["choices"][0]["message"]["content"].strip()
        questions = re.split(r"\n\s*\n", questions_text)  
        return questions[:n]  

    except Exception as e:
        print("⚠️ Perplexity API error:", e)
        return []


def generate_mcqs(text: str, n: int) -> List[Dict]:
    questions_raw = perplexity_generate_questions_batch(text, qtype="MCQ", n=n)
    mcqs = []

    for q_text in questions_raw:
        # Extract question stem
        stem_match = re.search(r"^(.*?)\n", q_text, re.DOTALL)
        stem = stem_match.group(1).strip() if stem_match else q_text.strip()

        # Extract options
        opts = re.findall(r"[A-D]\.\s*([^\n]+)", q_text)

        # Extract correct answer
        answer_match = re.search(r"Answer:\s*([A-D])", q_text, re.IGNORECASE)
        answer = opts[ord(answer_match.group(1).upper()) - 65] if opts and answer_match else None

        mcqs.append({
            "stem": stem,
            "options": opts if opts else [],
            "answer": answer
        })

    return mcqs

def generate_fibs(text: str, n: int) -> List[Dict]:
    questions_raw = perplexity_generate_questions_batch(text, qtype="FIB", n=n)
    fibs = []

    for q_text in questions_raw:
        answer_match = re.search(r"Answer:\s*(.+)", q_text)
        answer = answer_match.group(1) if answer_match else "_____"
        stem = re.sub(r"Answer:\s*.+", "_____", q_text).strip()
        fibs.append({"stem": stem, "answer": answer})

    return fibs

def generate_short_questions(text: str, n: int) -> List[str]:
    """
    Generate a list of individual short questions from the text.
    """
    # Get all short questions in batch (you can adjust n if needed)
    questions_raw = perplexity_generate_questions_batch(text, qtype="Short", n=n)
    
    # Split any multiple questions returned in a single string by numbering or newline
    short_questions = []
    for q in questions_raw:
        # Split by number or newline
        split_qs = re.split(r'\s*\d+\.\s+', q)
        for sq in split_qs:
            sq = sq.strip()
            if sq:  # ignore empty
                short_questions.append(sq)
    
    return short_questions[:n]


def generate_long_questions(text: str, n: int) -> List[str]:
    questions_raw = perplexity_generate_questions_batch(text, qtype="Long", n=n)
    return [q.strip() for q in questions_raw]

# =========================
# Main wrapper
# =========================
def clean_mcq_options(mcqs):
    letters = ['A', 'B', 'C', 'D']
    cleaned_mcqs = []

    for q in mcqs:
        opts = q.get("options", [])
        # Remove duplicates & empty strings
        opts = list(dict.fromkeys([opt.strip() for opt in opts if opt.strip()]))
        # Fill missing options
        while len(opts) < 4:
            opts.append("N/A")
        q["options"] = opts[:4]

       
        answer_text = q.get("answer")
        if answer_text and answer_text in opts:
            q["answer"] = letters[opts.index(answer_text)]
        else:
            q["answer"] = None  

        cleaned_mcqs.append(q)
    return cleaned_mcqs

def generate_question_paper(text: str = None, pdf_path: str = None, subject: str = "General",
                            counts: Dict[str,int] = None) -> dict:
    counts = counts or {"mcq": 10, "fib": 10, "short": 5, "long": 4}

    if pdf_path and os.path.isfile(pdf_path):
        text = extract_text_from_pdf(pdf_path)
        hash_hex = get_pdf_hash(pdf_path)
    else:
        text = text or SAMPLE_TEXT
        hash_hex = hashlib.sha256(text.encode()).hexdigest()

    text = clean_text(text)

    
    mcqs = generate_mcqs(text, counts.get("mcq", 10))
    mcqs = clean_mcq_options(mcqs)

    
    letters = ['A', 'B', 'C', 'D']
    for q in mcqs:
        if q.get("answer"):
            for i, opt in enumerate(q["options"]):
                if opt == q["answer"]:
                    q["answer"] = letters[i]
                    break

    return {
        "subject": subject,
        "hash": hash_hex,
        "questions_by_level": {
            "MCQ": mcqs,
            "FillBlanks": generate_fibs(text, counts.get("fib", 10)),
            "Short": generate_short_questions(text, counts.get("short", 5)),
            "Long": generate_long_questions(text, counts.get("long", 4)),
        }
    }


SAMPLE_TEXT = """Artificial Intelligence (AI) is the simulation of human intelligence in machines.
It involves creating intelligent systems capable of perceiving, reasoning, learning, and problem-solving.
AI has numerous real-world applications in healthcare, finance, transportation, and cybersecurity."""
