import re
import spacy

nlp = None

def get_nlp():
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")
    return nlp

def preprocess_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", " ", text)
    text = re.sub(r"#\w+", r" ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"([!?.,])\1{1,}", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()

    if text == "":
        return ""

    doc = get_nlp()(text)
    lemmas = []
    for token in doc:
        if token.ent_type_ in ("GPE", "LOC", "FAC"):
            continue
        if token.is_space or token.is_punct:
            continue
        lemmas.append(token.lemma_.lower())
    return " ".join(lemmas)