import streamlit as st
import re
from predict import predict_resume, match_resume_jd_bert, rank_candidates

st.set_page_config(page_title="AI Resume Screening", layout="centered")

# ---------------- VALIDATION ----------------
def is_valid_input(text):
    return bool(re.search(r"[a-zA-Z]{3,}", text))

valid_keywords = ["python", "sql", "machine learning", "ai", "data", "java", "deep learning"]

def has_valid_skills(text):
    return any(word in text.lower() for word in valid_keywords)

# ---------------- HEADER ----------------
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>
        AI Resume Screening System
    </h1>
    <hr>
""", unsafe_allow_html=True)

# ---------------- SECTION 1 ----------------
st.subheader("🔍 Resume Analyzer")

skills = st.text_input("💡 Enter Skills (comma separated)")
experience = st.slider("📊 Experience (years)", 0, 20, 0)
jd = st.text_area("📄 Enter Job Description")

if st.button("🚀 Analyze Resume"):

    if skills == "" or jd == "":
        st.warning("⚠️ Please enter Skills and Job Description")

    elif not is_valid_input(skills) or not is_valid_input(jd):
        st.error("❌ Invalid input")

    elif not has_valid_skills(skills):
        st.error("❌ Enter valid technical skills")

    else:
        role = predict_resume(skills, experience)
        match_score = match_resume_jd_bert(skills, jd)

        st.success(f"🎯 Predicted Role: {role}")

        if match_score > 70:
            st.success(f"🔥 Strong Match: {match_score}%")
        elif match_score > 40:
            st.warning(f"⚡ Moderate Match: {match_score}%")
        else:
            st.error(f"❌ Low Match: {match_score}%")

st.markdown("---")

# ---------------- SECTION 2 ----------------
st.subheader("🏆 Candidate Ranking System")

jd_rank = st.text_area("📄 Enter Job Description for Ranking")
num_candidates = st.slider("👥 Number of Candidates", 1, 5, 3)

candidates = []

for i in range(num_candidates):
    with st.expander(f"Candidate {i+1}"):
        name = st.text_input("Name", key=f"name_{i}")
        skills_c = st.text_input("Skills", key=f"skills_{i}")
        exp = st.slider("Experience", 0, 20, key=f"exp_{i}")

        candidates.append({
            "name": name,
            "skills": skills_c,
            "exp": exp
        })

if st.button("🏁 Rank Candidates"):

    if jd_rank == "":
        st.warning("⚠️ Enter Job Description")

    else:
        results = rank_candidates(candidates, jd_rank)

        if len(results) == 0:
            st.error("❌ No valid candidates")
        else:
            st.markdown("### 📊 Ranking Results")

            for i, r in enumerate(results):

                if i == 0:
                    st.success(f"🥇 Rank 1: {r['name']}")
                elif i == 1:
                    st.info(f"🥈 Rank 2: {r['name']}")
                elif i == 2:
                    st.warning(f"🥉 Rank 3: {r['name']}")
                else:
                    st.write(f"Rank {i+1}: {r['name']}")

                st.write(f"**Final Score:** {r['final_score']}")
                st.write(f"**Match Score:** {r['match_score']}%")
                st.write("---")