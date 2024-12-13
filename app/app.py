import os
import streamlit as st

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

# Function to save uploaded file
def save_uploaded_file(uploaded_file, file_path):
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

# Display File Uploads and Save them
if uploaded_file_1:
    file_path_1 = os.path.join(UPLOAD_DIR, uploaded_file_1.name)
    save_uploaded_file(uploaded_file_1, file_path_1)
    st.write(f"✅ Uploaded CV: **{uploaded_file_1.name}** (saved at {file_path_1})")

if uploaded_file_2:
    file_path_2 = os.path.join(UPLOAD_DIR, uploaded_file_2.name)
    save_uploaded_file(uploaded_file_2, file_path_2)
    st.write(f"✅ Uploaded Reason File: **{uploaded_file_2.name}** (saved at {file_path_2})")

# Analysis Button
if st.button("Start Bias Analysis"):
    if uploaded_file_1 and uploaded_file_2:
        st.success("Files uploaded and saved successfully! Starting analysis...", icon="📊")
        st.info("Analysis is under development. Stay tuned!", icon="🔄")
    else:
        st.error("Please upload both files before proceeding.", icon="⚠")
