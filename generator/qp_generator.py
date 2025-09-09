from typing import List, Dict, Tuple, Set
from collections import Counter, defaultdict
import hashlib
from PyPDF2 import PdfReader
import re
import nltk
from nltk.corpus import stopwords
from nltk import sent_tokenize, pos_tag, ne_chunk, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random 

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("taggers/averaged_perceptron_tagger")
except LookupError:
    nltk.download("averaged_perceptron_tagger")

try:
    nltk.data.find("chunkers/maxent_ne_chunker")
except LookupError:
    nltk.download("maxent_ne_chunker")

try:
    nltk.data.find("corpora/words")
except LookupError:
    nltk.download("words")

STOPWORDS = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    """Lowercase, remove extra spaces, keep only words & sentences."""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^A-Za-z0-9.,;:?!()\- ]", "", text)
    return text.strip()

def sentences(text: str) -> list[str]:
    """Split text into sentences using NLTK."""
    return sent_tokenize(text)

SAMPLE_TEXT = """Artificial Intelligence (AI) is the simulation of human intelligence 
in machines that are programmed to think like humans and mimic their actions. 
The term may also be applied to any machine that exhibits traits associated with 
a human mind such as learning and problem-solving."""

try:
    import spacy
    nlp = spacy.load("en_core_web_md")
    USE_SPACY = True
except Exception:
    from nltk.corpus import wordnet
    nlp = None
    USE_SPACY = False

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def normalize_token(t: str) -> str:
    return lemmatizer.lemmatize(t.lower())

def extract_named_entities(text: str) -> List[str]:
    """Extract named entities using NLTK."""
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    chunks = ne_chunk(pos_tags)
    
    entities = []
    for chunk in chunks:
        if hasattr(chunk, 'label'):
            entity = ' '.join([token for token, pos in chunk.leaves()])
            entities.append(entity)
    return entities

def find_key_concepts(text: str) -> List[str]:
    """Extract key concepts using multiple approaches."""
    concepts = []
    
    entities = extract_named_entities(text)
    concepts.extend(entities)
    
    sentences_list = sentences(text)
    for sent in sentences_list:
        tokens = word_tokenize(sent.lower())
        pos_tags = pos_tag(tokens)
        
        i = 0
        while i < len(pos_tags):
            word, tag = pos_tags[i]
            if tag in ['NN', 'NNS', 'NNP', 'NNPS'] and word not in STOPWORDS and len(word) > 2:
                compound = [word]
                j = i + 1
                while j < len(pos_tags) and pos_tags[j][1] in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']:
                    if pos_tags[j][0] not in STOPWORDS:
                        compound.append(pos_tags[j][0])
                    j += 1
                
                if len(compound) > 1:
                    concepts.append(' '.join(compound))
                    i = j
                elif len(word) > 4:  
                    concepts.append(word)
                    i += 1
                else:
                    i += 1
            else:
                i += 1
    
    seen = set()
    unique_concepts = []
    for concept in concepts:
        concept_lower = concept.lower()
        if concept_lower not in seen and len(concept.split()) <= 4:
            seen.add(concept_lower)
            unique_concepts.append(concept)
    
    return unique_concepts[:50]  

def analyze_sentence_relationships(sentences_list: List[str]) -> Dict[str, any]:
    """Analyze relationships between sentences using TF-IDF similarity."""
    if len(sentences_list) < 2:
        return {"similarity_matrix": None, "important_sentences": sentences_list}
    
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(sentences_list)
    
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    avg_similarity = np.mean(similarity_matrix, axis=1)
    sentence_scores = [(i, score, sent) for i, (score, sent) in enumerate(zip(avg_similarity, sentences_list))]
    sentence_scores.sort(key=lambda x: x[1], reverse=True)
    
    important_sentences = [sent for _, _, sent in sentence_scores[:min(20, len(sentence_scores))]]
    
    return {
        "similarity_matrix": similarity_matrix,
        "important_sentences": important_sentences,
        "sentence_scores": sentence_scores
    }

def identify_causal_relationships(text: str) -> List[Tuple[str, str]]:
    """Identify cause-effect relationships in text."""
    causal_patterns = [
        r"(.+?)\s+(?:causes?|leads? to|results? in|brings? about)\s+(.+?)[\.\,\;]",
        r"(?:because|since|due to)\s+(.+?)\s*,\s*(.+?)[\.\,\;]",
        r"(.+?)\s+(?:therefore|thus|consequently|as a result)\s+(.+?)[\.\,\;]",
        r"(?:if|when)\s+(.+?)\s*,\s*(?:then\s+)?(.+?)[\.\,\;]"
    ]
    
    relationships = []
    for pattern in causal_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            cause = match.group(1).strip()
            effect = match.group(2).strip()
            if len(cause) > 10 and len(effect) > 10 and len(cause) < 100 and len(effect) < 100:
                relationships.append((cause, effect))
    
    return relationships[:10] 

def generate_contextual_mcq(text: str, n: int) -> List[Dict]:
    """Generate MCQs based on content analysis and context."""
    concepts = find_key_concepts(text)
    sentences_list = sentences(text)
    analysis = analyze_sentence_relationships(sentences_list)
    causal_relations = identify_causal_relationships(text)
    
    mcqs = []
    used_concepts = set()
    
    for cause, effect in causal_relations[:n//3]:
        if len(mcqs) >= n:
            break
            
        stem = f"What is the primary result when {cause.lower()}?"
        correct_answer = effect.strip()
        
        distractors = []
        for other_cause, other_effect in causal_relations:
            if other_effect != effect and len(distractors) < 2:
                distractors.append(other_effect.strip())
        
        remaining_concepts = [c for c in concepts if c.lower() not in cause.lower() and c.lower() not in effect.lower()]
        while len(distractors) < 3 and remaining_concepts:
            distractors.append(remaining_concepts.pop(0))
        
        if len(distractors) >= 2:
            options = [correct_answer] + distractors[:3]
            random.shuffle(options)
            
            mcqs.append({
                "stem": stem,
                "options": options,
                "answer": correct_answer
            })
    
    important_sentences = analysis["important_sentences"]
    for sentence in important_sentences:
        if len(mcqs) >= n:
            break
            
        sentence_concepts = [c for c in concepts if c.lower() in sentence.lower()]
        if not sentence_concepts:
            continue
            
        concept = sentence_concepts[0]
      
            
        used_concepts.add(concept)
        
        if "define" in sentence.lower() or "definition" in sentence.lower():
            stem = f"How is {concept} best defined in this context?"
        elif "example" in sentence.lower() or "instance" in sentence.lower():
            stem = f"Which of the following best exemplifies {concept}?"
        elif "advantage" in sentence.lower() or "benefit" in sentence.lower():
            stem = f"What is a key advantage of {concept}?"
        elif "process" in sentence.lower() or "method" in sentence.lower():
            stem = f"What characterizes the process involving {concept}?"
        else:
            stem = f"According to the text, what is most important about {concept}?"
        
        concept_sentences = [s for s in sentences_list if concept.lower() in s.lower()]
        if concept_sentences:
            vectorizer = TfidfVectorizer(stop_words='english')
            concept_tfidf = vectorizer.fit_transform(concept_sentences)
            feature_names = vectorizer.get_feature_names_out()
            
            scores = concept_tfidf.sum(axis=0).A1
            top_indices = scores.argsort()[-5:][::-1]
            top_features = [feature_names[i] for i in top_indices if feature_names[i] != concept.lower()]
            
            if top_features:
                correct_answer = ' '.join(top_features[:2]).title()
            else:
                correct_answer = concept
        else:
            correct_answer = concept
        
        distractors = get_smart_distractors(correct_answer, concepts, sentence)
        
        if len(distractors) >= 2:
            options = [correct_answer] + distractors[:3]
            random.shuffle(options)
            
            mcqs.append({
                "stem": stem,
                "options": options,
                "answer": correct_answer
            })
    
    return mcqs[:n]

def get_smart_distractors(answer: str, concept_pool: List[str], context: str) -> List[str]:
    """Generate semantically plausible but incorrect distractors."""
    distractors = []
    
    pool = [c for c in concept_pool if c.lower() != answer.lower()]
    
    if USE_SPACY:
        answer_doc = nlp(answer)
        similarities = []
        
        for concept in pool:
            try:
                concept_doc = nlp(concept)
                sim = answer_doc.similarity(concept_doc)
                similarities.append((concept, sim))
            except:
                similarities.append((concept, 0.0))
        
        similarities.sort(key=lambda x: abs(x[1] - 0.3))  
        distractors = [c for c, _ in similarities[:4]]
    else:
        answer_tokens = word_tokenize(answer)
        answer_pos = set(tag for _, tag in pos_tag(answer_tokens))
        
        candidates = []
        for concept in pool:
            concept_tokens = word_tokenize(concept)
            concept_pos = set(tag for _, tag in pos_tag(concept_tokens))
            
            pos_overlap = len(answer_pos.intersection(concept_pos))
            length_diff = abs(len(answer.split()) - len(concept.split()))
            score = pos_overlap - length_diff * 0.5
            
            candidates.append((concept, score))
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        distractors = [c for c, _ in candidates[:4]]
    
    context_lower = context.lower()
    final_distractors = []
    
    for dist in distractors:
        if dist.lower() not in context_lower:
            final_distractors.append(dist)
        if len(final_distractors) >= 3:
            break
    
    return final_distractors

def generate_smart_fib(text: str, n: int) -> List[Dict]:
    """Generate fill-in-the-blank questions focusing on key information."""
    concepts = find_key_concepts(text)
    sentences_list = sentences(text)
    analysis = analyze_sentence_relationships(sentences_list)
    
    fib_questions = []
    used_concepts = set()
    
    for sentence in analysis["important_sentences"]:
        if len(fib_questions) >= n:
            break
            
        sentence_concepts = [c for c in concepts if c.lower() in sentence.lower() and c not in used_concepts]
        if not sentence_concepts:
            continue
        
        concept = max(sentence_concepts, key=lambda x: (len(x.split()), len(x)))
        used_concepts.add(concept)
        
       
        words = sentence.split()
        concept_words = concept.split()
        
        for i in range(len(words) - len(concept_words) + 1):
            if ' '.join(words[i:i+len(concept_words)]).lower() == concept.lower():
                blanked_sentence = ' '.join(words[:i] + ['_____'] + words[i+len(concept_words):])
                
                fib_questions.append({
                    "stem": blanked_sentence,
                    "answer": concept
                })
                break
    
    return fib_questions[:n]

def generate_analytical_short_questions(text: str, n: int) -> List[str]:
    """Generate short questions that require analysis and understanding."""
    concepts = find_key_concepts(text)
    causal_relations = identify_causal_relationships(text)
    
    questions = []
    
    analytical_templates = [
        "Explain how {concept} influences the overall process discussed.",
        "What are the key factors that determine the effectiveness of {concept}?",
        "Analyze the relationship between {concept} and its practical applications.",
        "Describe the conditions under which {concept} is most beneficial.",
        "What challenges might arise when implementing {concept}?",
        "Compare the advantages and limitations of {concept}.",
        "How does {concept} contribute to solving the main problem discussed?"
    ]
    
    for concept in concepts[:n]:
        if len(questions) >= n:
            break
        template = random.choice(analytical_templates)
        question = template.format(concept=concept)
        questions.append(question)
    
    causal_templates = [
        "Explain why {cause} leads to {effect}.",
        "What mechanisms connect {cause} to {effect}?",
        "Analyze the significance of the relationship between {cause} and {effect}."
    ]
    
    for cause, effect in causal_relations[:n//3]:
        if len(questions) >= n:
            break
        template = random.choice(causal_templates)
        question = template.format(cause=cause.strip(), effect=effect.strip())
        questions.append(question)
    
    return questions[:n]

def generate_comprehensive_long_questions(text: str, n: int) -> List[str]:
    """Generate comprehensive long-answer questions."""
    concepts = find_key_concepts(text)
    causal_relations = identify_causal_relationships(text)
    
    questions = []
    
    comprehensive_templates = [
        "Critically evaluate the role of {concept} in the context presented. Discuss its implications, challenges, and potential improvements.",
        "Analyze the interconnections between {concept} and related elements. How do these relationships affect overall outcomes?",
        "Design a comprehensive strategy incorporating {concept}. Justify your approach with evidence from the text and additional considerations.",
        "Examine the long-term consequences of implementing {concept}. What factors would determine success or failure?",
        "Compare and contrast different approaches to {concept}. Which would be most effective and why?",
        "Evaluate the theoretical foundations and practical applications of {concept}. What gaps exist in current understanding?"
    ]
    
    for concept in concepts[:n]:
        if len(questions) >= n:
            break
        template = random.choice(comprehensive_templates)
        question = template.format(concept=concept)
        questions.append(question)
    
    if causal_relations and len(questions) < n:
        system_questions = [
            f"Analyze the cause-and-effect relationships presented in the text. How do these interconnected factors create a system of dependencies?",
            f"Evaluate the overall framework described in the text. What are its strengths, weaknesses, and areas for improvement?",
            f"Design an implementation plan based on the concepts and relationships discussed. Address potential challenges and success metrics."
        ]
        
        questions.extend(system_questions[:n - len(questions)])
    
    return questions[:n]

def short_context(sentence: str, answer: str, max_words: int = 20) -> str:
    """Return a short, readable stem around the answer. If answer found, crop around it."""
    toks = sentence.split()
    lower = [t.lower().strip(".,;:()[]\"'") for t in toks]
    try:
        idx = lower.index(answer.lower())
    except ValueError:
        idx = None
        for i, tok in enumerate(lower):
            if normalize_token(tok) == normalize_token(answer):
                idx = i
                break
    if idx is None:
        stem = " ".join(toks[:max_words])
        if len(toks) > max_words:
            stem += "..."
        return stem
    left = max(0, idx - max_words//2)
    right = min(len(toks), left + max_words)
    stem = toks[left:right]
    stem[idx-left] = "_____"
    if left > 0:
        stem = ["..."] + stem
    if right < len(toks):
        stem = stem + ["..."]
    return " ".join(stem)

def unique_keep_order(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def make_cloze(sentence: str, answer: str) -> str:
    lower_tokens = [t.strip(".,;:()[]\"'") for t in sentence.split()]
    for i, t in enumerate(lower_tokens):
        if normalize_token(t) == normalize_token(answer):
            toks = sentence.split()
            toks[i] = "_____"
            return " ".join(toks)
    return short_context(sentence, answer, max_words=18)

def format_question_paper(subject: str, hash_hex: str, mcq_list, fib_list, short_list, long_list) -> str:
    lines = []
    lines.append("← Back\t\tPrint / Save as PDF\n")
    lines.append("="*72)
    lines.append(f"{subject.center(72)}")
    lines.append("="*72)
    lines.append(f"File Hash (SHA256): {hash_hex}\n")
    
    lines.append("Section A — Multiple Choice Questions (1 mark each)\n")
    for i, q in enumerate(mcq_list, start=1):
        lines.append(f"{i}. {q['stem']}")
        opts = q['options']
        labels = ['a','b','c','d']
        for lab, opt in zip(labels, opts):
            lines.append(f"    {lab}) {opt}")
        lines.append("")
    
    lines.append("\nSection B — Fill in the Blanks (1 mark each)\n")
    for i, f in enumerate(fib_list, start=1):
        lines.append(f"{i}. {f['stem']}")
    
    lines.append("\nSection C — Short Answer Questions (2 marks each)\n")
    for i, s in enumerate(short_list, start=1):
        lines.append(f"{i}. {s}")
    
    lines.append("\nSection D — Long Answer Questions (8 marks each)\n")
    for i, L in enumerate(long_list, start=1):
        lines.append(f"{i}. {L}")
    
    lines.append("\n" + "="*72)
    lines.append("Answer Key\n")
    lines.append("="*72)
    lines.append("MCQ Answers:")
    for i, q in enumerate(mcq_list, start=1):
        try:
            idx = q['options'].index(q['answer'])
            lab = ['a','b','c','d'][idx]
        except ValueError:
            lab = "?"
        lines.append(f"{i}. {lab}) {q['answer']}")
    
    lines.append("\nFIB Answers:")
    for i, f in enumerate(fib_list, start=1):
        lines.append(f"{i}. {f['answer']}")
    
    return "\n".join(lines)

def generate_question_paper(text: str, subject: str, counts: Dict[str, int], pdf_path_for_hash: str = None) -> dict:
    text = clean_text(text or SAMPLE_TEXT)
    if pdf_path_for_hash:
        hash_hex = get_pdf_hash(pdf_path_for_hash)
    else:
        hash_hex = hashlib.sha256(text.encode("utf-8")).hexdigest()

    mcq = generate_contextual_mcq(text, counts.get("mcq", 10))
    fib = generate_smart_fib(text, counts.get("fib", 10))
    short = generate_analytical_short_questions(text, counts.get("short", 5))
    long = generate_comprehensive_long_questions(text, counts.get("long", 4))

    return {
        "subject": subject,
        "hash": hash_hex,
        "questions_by_level": {
            "MCQ": mcq,
            "FillBlanks": fib,
            "Short": short,
            "Long": long
        }
    }

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract plain text from a PDF file."""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.strip()

def get_pdf_hash(pdf_path: str) -> str:
    """Compute SHA256 hash of a PDF file."""
    h = hashlib.sha256()
    with open(pdf_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
