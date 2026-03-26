import spacy

nlp = spacy.load("en_core_web_sm")


def process_with_spacy(text: str):
    doc = nlp(text)

    tokens = []

    for token in doc:
        # Skip unwanted tokens
        if token.is_stop or token.is_punct or token.is_space:
            continue

        # 🔥 Key Fix: selective lemmatization
        if token.pos_ == "VERB":
            tokens.append(token.lemma_.lower())
        else:
            tokens.append(token.text.lower())

    cleaned_text = " ".join(tokens)

    return cleaned_text, tokens