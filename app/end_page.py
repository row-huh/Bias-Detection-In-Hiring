import streamlit as st
from PyPDF2 import PdfReader
import os

# Set up the Streamlit page configuration
st.set_page_config(
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Load external CSS
with open("style.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# Load external HTML template (if needed)
with open("template.html") as html_file:
    st.markdown(html_file.read(), unsafe_allow_html=True)

# Directory where files are saved
UPLOAD_DIR = r"C:\\Users\\User\\Desktop\\neutral\\app\\uploaded_files"

# Function to extract text from a PDF
def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                return None  # If text extraction fails
        return text
    except Exception as e:
        return None

# File paths
cv_file_path = os.path.join(UPLOAD_DIR, "cv.pdf")
reason_file_path = os.path.join(UPLOAD_DIR, "reason.pdf")

# Display the results
if os.path.exists(cv_file_path) and os.path.exists(reason_file_path):
    # Extract text from the uploaded PDFs
    cv_text = extract_text_from_pdf(cv_file_path)
    reason_text = extract_text_from_pdf(reason_file_path)

    if cv_text:
        st.header("Uploaded CV")
        st.text_area("CV Content", cv_text, height=300, disabled=True)
    else:
        st.warning("Could not extract text from the CV PDF. It might be an image-based PDF.", icon="⚠")

    if reason_text:
        st.header("Reason for Not Hiring")
        st.text_area("Reason Content", reason_text, height=300, disabled=True)
    else:
        st.warning("Could not extract text from the Reason PDF. It might be an image-based PDF.", icon="⚠")

    # Placeholder for bias detection logic (example result)
    st.subheader("Bias Detection Outcome")

    # Example analysis logic (replace with actual implementation)
    is_biased = "Yes"  # Replace with actual analysis
    if is_biased == "Yes":
        st.error("The decision appears to be biased.", icon="⚠")
    else:
        st.success("The decision appears to be unbiased.", icon="✅")
else:
    st.error("Required files are missing in the specified directory.", icon="❌")
