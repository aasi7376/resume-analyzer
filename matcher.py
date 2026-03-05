import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text.lower())
    
    keywords = set(
        token.lemma_
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.is_space
        and token.is_alpha
        and len(token.text) > 2
    )
    
    return keywords


def match_keywords(resume_text, jd_text):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    matched = resume_keywords.intersection(jd_keywords)
    missing = jd_keywords.difference(resume_keywords)

    match_ratio = round((len(matched) / len(jd_keywords)) * 100, 2) if jd_keywords else 0

    return {
        "matched": sorted(list(matched)),
        "missing": sorted(list(missing)),
        "match_ratio": match_ratio,
        "total_jd_keywords": len(jd_keywords),
        "total_matched": len(matched),
    }