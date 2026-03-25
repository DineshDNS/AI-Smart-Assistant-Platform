import spacy

nlp = spacy.load("en_core_web_sm")


def process_with_spacy(text: str):
    doc = nlp(text)

    tokens = []
    for token in doc:
        if not token.is_stop and not token.is_punct:
            tokens.append(token.lemma_.lower())

    cleaned_text = " ".join(tokens)

    return cleaned_text, tokens