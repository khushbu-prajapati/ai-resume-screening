import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import streamlit as st

# ---------------- LOAD MODELS ----------------
@st.cache_resource
def load_bert_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

bert_model = load_bert_model()

model = joblib.load("resume_model.pkl")
tfidf = joblib.load("tfidf.pkl")
le_target = joblib.load("label_encoder.pkl")


# ---------------- HELPER ----------------
def exp_level(x):
    if x < 1:
        return 0
    elif x < 3:
        return 1
    elif x < 6:
        return 2
    else:
        return 3


# ---------------- ROLE PREDICTION ----------------
def predict_resume(skills_text, experience):

    skills_text = skills_text.lower().replace(" ", "")
    skills_text = " ".join(skills_text.split(","))

    skills_vector = tfidf.transform([skills_text])
    skills_df = pd.DataFrame(
        skills_vector.toarray(),
        columns=tfidf.get_feature_names_out()
    )

    exp = exp_level(experience)
    skills_count = len(skills_text.split())

    other = pd.DataFrame([[exp, skills_count]],
                         columns=['Experience_Level', 'Skills_Count'])

    final_input = pd.concat([skills_df, other], axis=1)

    pred = model.predict(final_input)
    role = le_target.inverse_transform(pred)

    return role[0]


# ---------------- BERT MATCHING ----------------
def match_resume_jd_bert(resume_text, jd_text):

    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    resume_embedding = bert_model.encode([resume_text], normalize_embeddings=True)
    jd_embedding = bert_model.encode([jd_text], normalize_embeddings=True)

    score = cosine_similarity(resume_embedding, jd_embedding)[0][0]

    # Normalize [-1,1] → [0,1]
    score = (score + 1) / 2
    score = max(0, min(score, 1))

    return float(round(score * 100, 2))


# ---------------- RANKING ----------------
def rank_candidates(candidates, jd_text):

    results = []

    for c in candidates:

        # skip empty inputs
        if not c["name"] or not c["skills"]:
            continue

        match_score = match_resume_jd_bert(c["skills"], jd_text)

        exp = c["exp"]

        if exp < 1:
            exp_score = 20
        elif exp < 3:
            exp_score = 50
        elif exp < 6:
            exp_score = 80
        else:
            exp_score = 100

        final = (0.7 * match_score) + (0.3 * exp_score)

        results.append({
            "name": c["name"],
            "match_score": round(match_score, 2),
            "exp_score": exp_score,
            "final_score": round(final, 2)
        })

    return sorted(results, key=lambda x: x["final_score"], reverse=True)