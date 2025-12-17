import re
import spacy
from spacy.symbols import ORTH

nlp = None
special = {"URLTOK", "EMAILTOK", "NUMTOK", "MENTIONTOK", "HASHTAGTOK"}

def get_nlp():
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        for tok in special:
            nlp.tokenizer.add_special_case(tok, [{ORTH: tok}])
    return nlp

def preprocess_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " URLTOK ", text)
    text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", " EMAILTOK ", text)
    text = re.sub(r"#(\w+)", r" HASHTAGTOK ", text)
    text = re.sub(r"@\w+", " MENTIONTOK ", text)
    text = re.sub(r"\d+", " NUMTOK ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if text == "":
        return ""

    doc = get_nlp()(text)
    lemmas = []
    for token in doc:
        if token.is_space or token.is_punct:
            continue

        t = token.text
        if t in special:
            lemmas.append(t.lower())
        else:
            lemmas.append(token.lemma_.lower())
    return " ".join(lemmas)