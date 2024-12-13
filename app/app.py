import os
import streamlit as st
import sys


# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)


from model.utility import *     # do not change this order

def main():
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

    # Initialize session state variables
    if 'file_path_1' not in st.session_state:
        st.session_state.file_path_1 = None
    if 'file_path_2' not in st.session_state:
        st.session_state.file_path_2 = None
    if 'analysis_started' not in st.session_state:
        st.session_state.analysis_started = False

    # Save and Display Uploaded Files
    if uploaded_file_1:
        st.session_state.file_path_1 = os.path.join(UPLOAD_DIR, 'cv.pdf')
        with open(st.session_state.file_path_1, "wb") as f:
            f.write(uploaded_file_1.getbuffer())
        st.write(f"✅ Uploaded CV: **{uploaded_file_1.name}** (saved at {st.session_state.file_path_1})")

    if uploaded_file_2:
        st.session_state.file_path_2 = os.path.join(UPLOAD_DIR, 'decision.pdf')
        with open(st.session_state.file_path_2, "wb") as f:
            f.write(uploaded_file_2.getbuffer())
        st.write(f"✅ Uploaded Reason File: **{uploaded_file_2.name}** (saved at {st.session_state.file_path_2})")

    # Analysis Button
    if st.button("Start Bias Analysis"):
        # Validate both files are uploaded
        if st.session_state.file_path_1 and st.session_state.file_path_2:
            st.session_state.analysis_started = True
            st.success("Files uploaded and saved successfully! Starting analysis...", icon="📊")
            st.info("Analysis is under development. Stay tuned!", icon="🔄")
        else:
            st.error("Please upload both files before proceeding.", icon="⚠")

    # Only return files if analysis has been started and both files are present
    if st.session_state.analysis_started and st.session_state.file_path_1 and st.session_state.file_path_2:
        send_to_llama(st.session_state.file_path_1, st.session_state.file_path_2)
    else:
        return None, None

def send_to_llama(cv_path, decision_path):

    print("PATHS:",cv_path, decision_path)

    cv = pdf_to_text(cv_path)
    decision = pdf_to_text(decision_path)

    print(cv)
    print(decision)

    #TODO
    # have llama convert the cv into columns
    # then have llama boil down the decision into 'hired' or 'not hired'
    # then have the ml predict the outcome
    # compare the outcomes, if the outcome matches the ml's outcome - then no bias
    # otherwise, bias detected




if __name__ == '__main__':
    main()