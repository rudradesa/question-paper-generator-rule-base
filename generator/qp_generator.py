import re
import random
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
import PyPDF2
import hashlib
import nltk
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet

# Try to ensure required resources exist
def _safe_download(pkg_list):
    try:
        for p in pkg_list:
            try:
                nltk.data.find(p)
            except LookupError:
                # map resource hints to download names
                name = p.split("/")[-1]
                nltk.download(name)
    except Exception:
        pass

_safe_download([
    "tokenizers/punkt",
    "taggers/averaged_perceptron_tagger",
    "corpora/wordnet",
    "corpora/stopwords",
])

STOPWORDS = set(stopwords.words("english"))
WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-']+")

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF file"""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return clean_text(text)

def get_pdf_hash(pdf_path: str) -> str:
    """Generate SHA256 hash of a PDF file"""
    hasher = hashlib.sha256()
    with open(pdf_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def clean_text(text: str) -> str:
    # Light cleanup
    text = re.sub(r"\s+", " ", text).strip()
    return text

def sentences(text: str) -> List[str]:
    try:
        sents = sent_tokenize(text)
    except LookupError:
        nltk.download("punkt")
        sents = sent_tokenize(text)
    return [s.strip() for s in sents if len(s.strip().split()) >= 5]

def tokenize_words(text: str) -> List[str]:
    tokens = [t for t in word_tokenize(text) if WORD_RE.fullmatch(t)]
    return tokens

def keyword_candidates(text: str, top_k: int = 60) -> List[str]:
    """Return top_k frequent nouns/adjectives as keyword candidates."""
    tokens = [t.lower() for t in tokenize_words(text)]
    if not tokens:
        return []
    tagged = pos_tag(tokens)
    keep_pos = {"NN","NNS","NNP","NNPS","JJ","JJR","JJS"}
    c = Counter([w for w, p in tagged if p in keep_pos and w not in STOPWORDS and len(w) > 2])
    return [w for w, _ in c.most_common(top_k)]

def pick_sentences_with_keywords(sents: List[str], keywords: List[str]) -> Dict[str, List[str]]:
    idx = defaultdict(list)
    for s in sents:
        low = s.lower()
        for k in keywords:
            if f" {k} " in f" {low} ":
                idx[k].append(s)
    return idx

def wordnet_distractors(answer: str, pool: List[str], k: int = 3) -> List[str]:
    distractors = set()
    try:
        syns = wordnet.synsets(answer)
        lemmas = set()
        for s in syns:
            for l in s.lemmas():
                lemmas.add(l.name().replace("_", " ").lower())
        candidates = [w for w in pool if w != answer and w not in lemmas]
        random.shuffle(candidates)
        for w in candidates:
            if len(distractors) >= k:
                break
            distractors.add(w)
    except Exception:
        pass
    # Fallback purely from pool if WordNet empty
    if len(distractors) < k:
        choices = [w for w in pool if w != answer]
        random.shuffle(choices)
        for w in choices:
            if len(distractors) >= k:
                break
            distractors.add(w)
    return list(distractors)[:k]

def make_cloze(sentence: str, answer: str) -> str:
    pattern = re.compile(re.escape(answer), re.IGNORECASE)
    q = pattern.sub("_____", sentence, count=1)
    return q

def generate_mcq(text: str, n: int) -> List[Dict]:
    text = clean_text(text)
    sents = sentences(text)
    keys = keyword_candidates(text, top_k=80)
    sent_index = pick_sentences_with_keywords(sents, keys)

    mcqs = []
    used_answers = set()
    for k in keys:
        if len(mcqs) >= n:
            break
        s_list = sent_index.get(k, [])
        if not s_list:
            continue
        answer = k
        if answer in used_answers:
            continue
        s = random.choice(s_list)
        question = make_cloze(s, answer)
        distractor_pool = [w for w in keys if w != answer][:50]
        options = wordnet_distractors(answer, distractor_pool, k=3) + [answer]
        random.shuffle(options)
        mcqs.append({
            "question": question,
            "options": options,
            "answer": answer
        })
        used_answers.add(answer)

    # Fallback: if not enough, create generic MCQs from top keys
    i = 0
    while len(mcqs) < n and i < len(keys):
        answer = keys[i]
        i += 1
        if answer in used_answers:
            continue
        question = f"Which of the following is most closely related to the topic discussed?"
        distractor_pool = [w for w in keys if w != answer][:50]
        options = wordnet_distractors(answer, distractor_pool, k=3) + [answer]
        random.shuffle(options)
        mcqs.append({"question": question, "options": options, "answer": answer})
        used_answers.add(answer)

    return mcqs[:n]

def generate_fib(text: str, n: int) -> List[Dict]:
    text = clean_text(text)
    sents = sentences(text)
    keys = keyword_candidates(text, top_k=100)
    out = []
    used = set()

    for s in sents:
        if len(out) >= n:
            break
        # choose a keyword present in this sentence
        low = s.lower()
        candidates = [k for k in keys if f" {k} " in f" {low} " and k not in used]
        if not candidates:
            continue
        ans = random.choice(candidates)
        q = make_cloze(s, ans)
        out.append({"question": q, "answer": ans})
        used.add(ans)

    # Fallback generic if needed
    while len(out) < n and keys:
        ans = keys[len(out) % len(keys)]
        q = f"Fill in the blank: The key concept in this topic is _____."
        out.append({"question": q, "answer": ans})
    return out[:n]

def generate_short_questions(text: str, n: int) -> List[str]:
    keys = keyword_candidates(text, top_k=50)[:max(10, n*2)]
    templates = [
        "What is {k}?",
        "List any two features of {k}.",
        "Why is {k} important?",
        "Give a real-world example of {k}.",
        "Differentiate {k} from related concepts."
    ]
    qs = []
    i = 0
    while len(qs) < n and i < len(keys):
        k = keys[i]
        for t in templates:
            if len(qs) >= n:
                break
            qs.append(t.format(k=k))
        i += 1
    return qs[:n]

def generate_long_questions(text: str, n: int) -> List[str]:
    keys = keyword_candidates(text, top_k=30)[:max(8, n*2)]
    templates = [
        "Explain {k} in detail. Discuss its components and applications.",
        "Describe the working of {k} with a neat diagram and suitable examples.",
        "Critically analyze the advantages, limitations, and use-cases of {k}.",
        "Discuss the architecture and workflow of {k}, highlighting challenges and solutions."
    ]
    random.shuffle(templates)
    qs = []
    i = 0
    while len(qs) < n and i < len(keys):
        k = keys[i]
        for t in templates:
            if len(qs) >= n:
                break
            qs.append(t.format(k=k))
        i += 1
    return qs[:n]

# --- New Logic for Upper / Middle / Lower split ---
def split_questions_by_level(all_questions: List) -> Dict[str, List]:
    """
    Split questions into Upper (top 30%), Middle (middle 40%), Lower (bottom 30%).
    Works on any list of questions.
    """
    total = len(all_questions)
    if total == 0:
        return {
            "Upper (top 30%)": [],
            "Middle (middle 40%)": [],
            "Lower (bottom 30%)": []
        }

    upper_end = int(0.3 * total)
    middle_end = upper_end + int(0.4 * total)

    return {
        "Upper (top 30%)": all_questions[:upper_end],
        "Middle (middle 40%)": all_questions[upper_end:middle_end],
        "Lower (bottom 30%)": all_questions[middle_end:]
    }

def generate_question_paper(text: str, subject: str, counts: Dict[str, int]) -> Dict:
    text = clean_text(text or "")
    if not text:
        # Provide a helpful default using bundled sample
        text = SAMPLE_TEXT
    mcq = generate_mcq(text, counts.get("mcq", 10))
    fib = generate_fib(text, counts.get("fib", 10))
    short_q = generate_short_questions(text, counts.get("short", 5))
    long_q = generate_long_questions(text, counts.get("long", 4))

    # Combine all into one list for level splitting
    all_questions = []
    all_questions.extend(mcq)
    all_questions.extend(fib)
    all_questions.extend(short_q)
    all_questions.extend(long_q)

    # Split into levels
    level_split = split_questions_by_level(all_questions)

    return {
        "subject": subject,
        "questions_by_level": level_split
    }

# A tiny sample text (used when no input is provided)
SAMPLE_TEXT = """Computer networks enable devices to exchange data using links such as cables, Wi-Fi, or optical fiber.
Routers forward packets between networks using routing tables and protocols like OSPF and BGP.
The TCP/IP model includes layers such as application, transport, internet, and link.
Switches operate at the data link layer to build MAC address tables and segment collision domains.
DNS resolves human-readable domain names to IP addresses, while DHCP assigns IP configurations dynamically.
Firewalls filter traffic based on rules to improve security, and NAT translates private addresses.
"""
