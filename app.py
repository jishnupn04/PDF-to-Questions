import requests
import streamlit as st

st.title("PDF Question Generator")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"], accept_multiple_files=False)

marks = st.number_input("Enter Marks Per Question", min_value=1, max_value=20, value=5)

if st.button("Generate Questions"):
    if uploaded_file:
        files = {"pdf": uploaded_file}
        data = {"marks": marks}
        response = requests.post("http://127.0.0.1:8000/api/upload_pdf/", files=files, data=data)

        if response.status_code == 200:
            questions = response.json().get("questions", "No questions generated.")
            st.text_area("Generated Questions", questions, height=300)
        else:
            st.error("Error generating questions. Please try again.")
