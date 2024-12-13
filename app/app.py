import os
import streamlit as st
from model.utility import *


def upload_and_analyze_files():
    # Set up the Streamlit page configuration
    st.set_page_config(
        page_title="Neutral - Bias Detection",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Load external CSS
    with open("static/style.css") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

    # Load external HTML template
    with open("templates/template.html") as html_file:
        st.markdown(html_file.read(), unsafe_allow_html=True)

    # Directory where files will be saved
    UPLOAD_DIR = "uploads"

    # Create the upload directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # File Upload Section
    uploaded_file_1 = st.file_uploader("Step 1: Upload Your CV (PDF format only)", type="pdf")
    uploaded_file_2 = st.file_uploader("Step 2: Upload the Company's Reason for Not Hiring (PDF format only)", type="pdf")

    file_path_1, file_path_2 = None, None

    # Save and Display Uploaded Files
    if uploaded_file_1:
        file_path_1 = os.path.join(UPLOAD_DIR, 'cv.pdf')
        with open(file_path_1, "wb") as f:
            f.write(uploaded_file_1.getbuffer())
        st.write(f"✅ Uploaded CV: **{uploaded_file_1.name}** (saved at {file_path_1})")

    if uploaded_file_2:
        file_path_2 = os.path.join(UPLOAD_DIR, 'decision.pdf')
        with open(file_path_2, "wb") as f:
            f.write(uploaded_file_2.getbuffer())
        st.write(f"✅ Uploaded Reason File: **{uploaded_file_2.name}** (saved at {file_path_2})")

    # Analysis Button
    if st.button("Start Bias Analysis"):
        if file_path_1 and file_path_2:
            st.success("Files uploaded and saved successfully! Starting analysis...", icon="📊")
            st.info("Analysis is under development. Stay tuned!", icon="🔄")
        else:
            st.error("Please upload both files before proceeding.", icon="⚠")

    return file_path_1, file_path_2

def main():
    # ensure that the user has uploaded files
    cv_path, decision_path = upload_and_analyze_files()

    cv = pdf_to_text(cv_path)
    decision = pdf_to_text(decision_path)


    print(cv)

    print("*******************")

    print(decision)




if __name__ == '__main__':
    main()