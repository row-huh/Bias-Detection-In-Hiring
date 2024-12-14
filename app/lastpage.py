import os
import streamlit as st
import sys
from model.utility import *  # DO NOT change this
from model.genai import *
  # Example helper function for bias analysis
import requests

# Ensure the 'requests' module is available
print(f"Requests is available: {hasattr(requests, 'get')}")

# ... (Rest of your code remains unchanged)

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Constants
UPLOAD_DIR = "uploads"

# Ensure upload directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


def main():
    # Page Configuration
    st.set_page_config(
        page_title="Bias Analysis Results",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.title("Bias Detection Results")
    st.write("Here are the results of your bias analysis.")

    # Validate that the session contains uploaded files
    if 'file_path_1' in st.session_state and 'file_path_2' in st.session_state:
        cv_path = st.session_state.file_path_1
        decision_path = st.session_state.file_path_2

        # Extract text from PDFs
        cv_text = pdf_to_text(cv_path)
        decision_text = pdf_to_text(decision_path)

        # Display extracted content previews
        st.subheader("Uploaded CV Content Preview:")
        st.text_area("CV Text", value=cv_text[:500], height=200)

        st.subheader("Company's Decision Content Preview:")
        st.text_area("Company's Reason Text", value=decision_text[:500], height=200)

        # Perform bias analysis
        st.subheader("Bias Analysis Results")
        cv_bias_score, decision_bias_score = analyze_bias(cv_text, decision_text)

        # Display bias scores
        st.write(f"📄 **CV Bias Score:** {cv_bias_score}%")
        st.write(f"📑 **Company's Reason Bias Score:** {decision_bias_score}%")

        # Interpretation of bias scores
        if cv_bias_score > 60:
            st.warning("⚠️ The CV contains significant biased language.")
        elif cv_bias_score > 40:
            st.info("The CV contains some biased elements but is relatively balanced.")
        else:
            st.success("✅ The CV appears neutral and unbiased.")

        if decision_bias_score > 60:
            st.warning("⚠️ The company's reason contains significant biased language.")
        elif decision_bias_score > 40:
            st.info("The company's reason contains some biased elements but is relatively balanced.")
        else:
            st.success("✅ The company's reason appears neutral and unbiased.")

        # Visual progress bars
        st.progress(cv_bias_score / 100)
        st.progress(decision_bias_score / 100)

    else:
        st.error("No files detected! Please upload your CV and company's reason first from the landing page.")


# Example bias analysis function
def analyze_bias(cv_text, decision_text):
    """
    Analyze bias in CV and company's decision text based on predefined keywords.
    Returns bias scores for both inputs.
    """
    biased_keywords = ['discrimination', 'prejudice', 'biased', 'favoritism', 'stereotype']
    neutral_keywords = ['fairness', 'neutral', 'unbiased', 'impartial', 'equal']

    def calculate_score(text):
        biased_count = sum(1 for word in biased_keywords if word in text.lower())
        neutral_count = sum(1 for word in neutral_keywords if word in text.lower())
        total = biased_count + neutral_count
        if total == 0:
            return 50  # Default score if no keywords are found
        return (biased_count / total) * 100

    cv_score = calculate_score(cv_text)
    decision_score = calculate_score(decision_text)
    return round(cv_score, 2), round(decision_score, 2)


if __name__ == "__main__":
    main()
