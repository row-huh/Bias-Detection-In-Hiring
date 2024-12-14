import os
import streamlit as st
import sys
import PyPDF2

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from model.utility import *  # do not change this
from model.genai import *  # Make sure this import works and provides necessary functions

# Directory where files will be saved
UPLOAD_DIR = "uploads"

<<<<<<< HEAD
# Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Function to extract text from PDF files
def pdf_to_text(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to handle the file uploads and store them in session state
def handle_file_upload(uploaded_file_1, uploaded_file_2):
    if uploaded_file_1:
        file_path_1 = os.path.join(UPLOAD_DIR, 'cv.pdf')
        with open(file_path_1, "wb") as f:
            f.write(uploaded_file_1.getbuffer())
        st.session_state.file_path_1 = file_path_1
        st.write(f"✅ Uploaded CV: **{uploaded_file_1.name}** (saved at {file_path_1})")

    if uploaded_file_2:
        file_path_2 = os.path.join(UPLOAD_DIR, 'decision.pdf')
        with open(file_path_2, "wb") as f:
            f.write(uploaded_file_2.getbuffer())
        st.session_state.file_path_2 = file_path_2
        st.write(f"✅ Uploaded Reason File: **{uploaded_file_2.name}** (saved at {file_path_2})")

# Function to perform the bias analysis and interaction with the AI
def send_to_ai(cv_path, decision_path):
    # Extract text from both PDF files
    cv_text = pdf_to_text(cv_path)
    decision_text = pdf_to_text(decision_path)

    # Prepare request for AI (you need to define how your AI should process the text)
    user_req = f'''Turn the text delimited by triple backticks into the following columns:
    S.No,Age,Accessibility,EdLevel,Employment,Gender,MentalHealth,MainBranch,YearsCode,YearsCodePro,Country,PreviousSalary,HaveWorkedWith,ComputerSkills,Employed,Age_Category,Is_Employed,Skills_List,Skills_Count,Education_Level,Gender_Category,Previous_Salary,Years_Coding,Years_Professional_Coding
    ```{cv_text}``` 
    RESPOND IN ONLY CSV VALUE - NO ADDITIONAL TEXT, ONLY THE VALUES IN COMMA SEPARATED FORMAT, DO NOT INCLUDE THE COLUMN NAMES EITHER 
    '''

    ai = AI(SYSTEM_PROMPT)
    new_columns = ai.generate_response(user_req)

    # Additional AI processing, such as comparing predicted outcomes
    print(f"NEW COLUMNS: {new_columns}")
    # You can now process the bias detection based on this AI response

# Main function to control the logic
=======
>>>>>>> 03722b9b2f9ccf183ab14f9704286cea96f6ed53
def main():
    # Set up the Streamlit page configuration
    st.set_page_config(
        page_title="Neutral - Bias Detection",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Load external CSS and HTML templates (if any)
    with open("static/style.css") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

    with open("templates/template.html") as html_file:
        st.markdown(html_file.read(), unsafe_allow_html=True)

    # File Upload Section
    uploaded_file_1 = st.file_uploader("Step 1: Upload Your CV (PDF format only)", type="pdf")
    uploaded_file_2 = st.file_uploader("Step 2: Upload the Company's Reason for Not Hiring (PDF format only)", type="pdf")

    # Handle file uploads
    handle_file_upload(uploaded_file_1, uploaded_file_2)

    # Initialize session state variables if they are not already set
    if 'file_path_1' not in st.session_state:
        st.session_state.file_path_1 = None
    if 'file_path_2' not in st.session_state:
        st.session_state.file_path_2 = None
    if 'analysis_started' not in st.session_state:
        st.session_state.analysis_started = False

    # Start analysis button
    if st.button("Start Bias Analysis"):
        # Validate if both files are uploaded
        if st.session_state.file_path_1 and st.session_state.file_path_2:
            st.session_state.analysis_started = True
            st.success("Files uploaded and saved successfully! Starting analysis...", icon="📊")
            st.info("Analysis is under development. Stay tuned!", icon="🔄")
        else:
            st.error("Please upload both files before proceeding.", icon="⚠")

    # If analysis has been started, send files to AI for processing
    if st.session_state.analysis_started and st.session_state.file_path_1 and st.session_state.file_path_2:
        send_to_ai(st.session_state.file_path_1, st.session_state.file_path_2)
    else:
        return None, None

<<<<<<< HEAD
=======

def send_to_ai(cv_path, decision_path):

    print("PATHS:",cv_path, decision_path)

    cv = pdf_to_text(cv_path)
    decision = pdf_to_text(decision_path)

    user_req = f'''Turn the text delimited by triple backticks into the following columns:
    S.No,Age,Accessibility,EdLevel,Employment,Gender,MentalHealth,MainBranch,YearsCode,YearsCodePro,Country,PreviousSalary,HaveWorkedWith,ComputerSkills,Employed,Age_Category,Is_Employed,Skills_List,Skills_Count,Education_Level,Gender_Category,Previous_Salary,Years_Coding,Years_Professional_Coding
    ```{cv}```
    RESPOND IN ONLY CSV VALUE - NO ADDITIONAL TEXT, ONLY THE VALUES IN COMMA SEPARATED FORMAT, DO NOT INCLUDE THE COLUMN NAMES EITHER 
    '''

    ai = AI(SYSTEM_PROMPT)

    new_columns = ai.generate_response(user_req)

    print(f"NEW COLUMNS: {new_columns}")

    # ml_decision = get_ml_decision(new_columns)
    ml_decision = 'BIASED'

    new_prompt = f""" 
    You know the following things
    CV (delimited by triple backticks) : ```{cv}```,
    Decision (delimited by double backticks): ``{decision}``,
    You also have a prediction from an expert machine learning system that determined the following decision as {ml_decision}
    
    Now write 500 words explaining why the following decision for the following candidate (the one whose cv is given) might be biased or might be a justfied decision.
    Remember to always trust the machine learning's decision - it's been trained for this purpose and is more accurate
"""

    document = ai.generate_response(new_prompt)

    print(document)


    #TODO
    # have llama convert the cv into columns
    # then have llama boil down the decision into 'hired' or 'not hired'
    # then have the ml predict the outcome
    # compare the outcomes, if the outcome matches the ml's outcome - then no bias
    # otherwise, bias detected


>>>>>>> 03722b9b2f9ccf183ab14f9704286cea96f6ed53
if __name__ == '__main__':
    main()
