import os
import streamlit as st
import sys
from lastpage import final_analysis
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)


from app.utility import *     # do not change this 
from model.genai import *


def first_page():
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

        # Return file paths only if both files are uploaded
        return st.session_state.file_path_1, st.session_state.file_path_2


def final_analysis(analysis: str):
    """
    Displays the given analysis on a Streamlit page with the heading 'Neutral's Analysis Result' 
    and provides a button to download the analysis as a PDF.

    Parameters:
        analysis (str): The analysis text to display and download.
    """

    # Clear existing page content
    st.session_state.clear_page = st.empty()

    # Render header bar
    st.markdown(
        """
        <style>
            .header-bar {
                background-color: #008080; /* Teal color */
                padding: 10px;
                color: white;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
            }
        </style>
        <div class="header-bar">Neutral</div>
        """,
        unsafe_allow_html=True,
    )

    # Page content
    st.title("Detecting Biases in Hiring")
    st.header("Neutral's Analysis Result")
    st.markdown(
        f"""
        <div style="background-color: #222; color: #ddd; padding: 15px; border-radius: 5px;">
            <p style="font-size: 16px;">{analysis}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Generate PDF and Download
    if st.button("Generate PDF"):
        pdf_stream = BytesIO()
        c = canvas.Canvas(pdf_stream, pagesize=letter)
        c.drawString(72, 750, "Neutral's Analysis Result")
        c.drawString(72, 730, "Analysis:")
        y = 710
        line_height = 14
        for line in analysis.splitlines():
            c.drawString(72, y, line)
            y -= line_height
            if y < 50:  # Start a new page if needed
                c.showPage()
                y = 750
        c.save()
        pdf_stream.seek(0)
        st.download_button(
            label="Download PDF",
            data=pdf_stream.getvalue(),
            file_name="analysis_result.pdf",
            mime="application/pdf",
        )



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

    return document

def main():
    # Initialize the session state variable for page control
    if 'page' not in st.session_state:
        st.session_state.page = 'first'

    # Show the appropriate page based on the session state
    if st.session_state.page == 'first':
        file_path_1, file_path_2 = first_page()
        
        # Proceed only if analysis has started and both files are uploaded
        if st.session_state.get('analysis_started') and file_path_1 and file_path_2:
            # Perform the analysis
            analysis_result = send_to_ai(file_path_1, file_path_2)  # Replace with your analysis logic
            
            # Clear the page and show the final analysis page
            st.session_state.page = 'final'  # Update page state
            final_analysis(analysis_result)
    elif st.session_state.page == 'final':
        # If we're on the final page, just display it
        if 'analysis_result' in st.session_state:
            final_analysis('oh')

if __name__ == '__main__':
    main()