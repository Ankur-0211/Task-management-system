import streamlit as st
import joblib

# Load vectorizer and models
vectorizer = joblib.load("tfidf_vectorizer.pkl")
task_model = joblib.load("task_model.pkl")
priority_model = joblib.load("priority_model.pkl")

# Label mappings
task_type_labels = {
    0: "Development",
    1: "Design",
    2: "Marketing",
    3: "Documentation",
    4: "General"
}

priority_labels = {
    0: "Low",
    1: "Medium",
    2: "High"
}

# Streamlit page settings
st.set_page_config(page_title="Task Type & Priority Predictor", layout="centered")
st.title("📌 Task Type & Priority Predictor")
st.markdown("Enter your task **description** to predict its **category** and **priority level** using ML.")

    
    
# Input
st.subheader("📝 Task Description")
description = st.text_area("Enter the task details here", height=160)

# Predict button
if st.button("🚀 Predict"):
    if not description.strip():
        st.warning("Please enter a task description to get predictions.")
    else:
        # Vectorize description
        desc_vector = vectorizer.transform([description])

        # Model predictions
        task_type_pred = task_model.predict(desc_vector)[0]
        priority_pred = priority_model.predict(desc_vector)[0]

        # Display results
        st.markdown("## 🔍 Prediction Results")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📂 Task Type**")
            st.success(task_type_labels.get(task_type_pred, "Unknown"))

        with col2:
            st.markdown("**⚠️ Priority Level**")
            st.info(priority_labels.get(priority_pred, "Unknown"))
