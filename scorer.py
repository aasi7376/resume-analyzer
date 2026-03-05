from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(resume_processed, jd_processed):
    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform([resume_processed, jd_processed])

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    score = round(float(similarity[0][0]) * 100, 2)
    
    return score