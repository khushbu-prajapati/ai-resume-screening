# 🚀 AI Resume Screening System

An end-to-end AI-powered Resume Screening System that predicts job roles, matches resumes with job descriptions using BERT, and ranks candidates based on relevance.

---

## 🔥 Live Demo

👉 https://your-app-link.streamlit.app
*(Replace this with your deployed link)*

---

## 🧠 Features

* 🎯 **Job Role Prediction**

  * Predicts suitable job role based on candidate skills
  * Built using Machine Learning (XGBoost)

* 📊 **Resume vs Job Description Matching**

  * Uses BERT-based semantic similarity
  * Provides match percentage score

* 🏆 **Candidate Ranking System**

  * Ranks multiple candidates based on:

    * JD match score
    * Experience level

* 🖥️ **Interactive UI**

  * Built using Streamlit
  * Simple and recruiter-friendly interface

---

## 🛠️ Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn
* XGBoost
* Sentence Transformers (BERT)
* Streamlit

---

## ⚙️ How It Works

1. User enters candidate skills and experience
2. ML model predicts the most suitable job role
3. BERT compares resume with job description
4. System calculates similarity score
5. Candidates are ranked based on final score

---

## 📂 Project Structure

├── app.py
├── predict.py
├── resume_model.pkl
├── tfidf.pkl
├── label_encoder.pkl
├── requirements.txt
└── README.md

---

## ▶️ Run Locally

git clone https://github.com/your-username/ai-resume-screening.git
cd ai-resume-screening
pip install -r requirements.txt
streamlit run app.py

---

## 💡 Sample Input

Skills: Python, SQL, Machine Learning
Experience: 2 years
Job Description: Looking for a Data Scientist with experience in Python, SQL, and ML

---

## 📈 Future Improvements

* Resume PDF parsing
* Advanced NLP preprocessing
* Explainable AI
* Database integration
* Authentication system

---

## 👩‍💻 Author

Khushbu Prajapati

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
