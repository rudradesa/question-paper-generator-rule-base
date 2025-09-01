# Question Paper Generator (Flask + Python + HTML/CSS)

A simple end‑to‑end app that generates a question paper from input text:
- 10 MCQs
- 10 Fill in the Blanks (FIB)
- 5 Short Answers
- 4 Long Answers

The NLP is rule‑based using NLTK (lightweight, no heavy models). You can later plug in spaCy/transformers.

---

## 1) Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

# First run, download NLTK data (done automatically on first import)
python -c "import nltk; [nltk.download(pkg) for pkg in ['punkt','punkt_tab','averaged_perceptron_tagger','averaged_perceptron_tagger_eng','wordnet','stopwords']]"
```

> Note: Some NLTK package names vary by version; the app also tries to download missing ones at runtime.

## 2) Run the app

```bash
python app.py
```
Open http://localhost:5000 in your browser.

## 3) How it works (NLP steps, easy version)

1. **Clean & tokenize** the text → sentences & words (NLTK).
2. **Score keywords** using TF (term frequency) of nouns/adjectives, ignoring stopwords.
3. **MCQ**
   - Pick top keywords as answers.
   - Find sentences containing those answers.
   - Make a cloze question by blanking the answer.
   - Create 3 distractors from other top keywords / WordNet neighbors.
4. **FIB**
   - Choose sentences with strong keywords and blank one keyword.
5. **Short Qs**
   - Template prompts from top keywords (e.g., *"What is X?"*).
6. **Long Qs**
   - Broader prompts like *"Explain X in detail with examples."*

This is intentionally simple so it works out‑of‑the‑box. Improve by swapping in spaCy + YAKE/KeyBERT and better distractor generation.

## 4) API

`POST /api/generate`

```json
{
  "text": "paste your syllabus or chapter here",
  "subject": "Computer Networks",
  "mcq": 10, "fib": 10, "short": 5, "long": 4
}
```

Returns JSON with `mcq`, `fib`, `short`, `long` sections.

## 5) Print / Export

Use the **Print** button in the UI to save as PDF (browser print dialog). A dedicated DOCX export can be added later.

## 6) Tips to get better papers

- Give clean, topic‑focused input (remove headings like "Objectives").
- Feed at least a few paragraphs; more context → better questions.
- Edit the output — auto‑generated papers are a starting point.
