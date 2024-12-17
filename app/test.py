import streamlit as st
import os
import sys
import docx
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io
from utility import *

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)


from model.genai import *



def first_page():
    """
    Creates the first page with file upload functionality.
    Returns two placeholder strings for demonstration.
    """
    # Set up the Streamlit page configuration
    st.set_page_config(
        page_title="Neutral - Bias Detection",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # st.title("File Upload Page")
    
    # Load external CSS
    with open("static/style.css") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

    # Load external HTML template
    with open("templates/template.html") as html_file:
        st.markdown(html_file.read(), unsafe_allow_html=True)


    # File upload for CV
    cv_file = st.file_uploader("Upload CV", type=['pdf', 'docx', 'txt'])
    
    # File upload for decision document
    decision_file = st.file_uploader("Upload Decision Document", type=['pdf', 'docx', 'txt'])
    
    # Analyze button
    if st.button("Analyze Documents"):
        # Store files in session state
        st.session_state.cv_file = cv_file
        st.session_state.decision_file = decision_file
        
        # Switch to analysis page
        st.session_state.page = 'analysis'
        
        # Use st.rerun() instead of experimental_rerun()
        st.rerun()
    
    return file_to_text(cv_file), file_to_text(decision_file)

def create_analysis_pdf(analysis):
    """
    Create a PDF file from the analysis text.
    
    Args:
        analysis (str): The analysis text to be converted to PDF
    
    Returns:
        bytes: PDF file content in bytes
    """
    # Create a BytesIO buffer to store the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                            rightMargin=72, leftMargin=72, 
                            topMargin=72, bottomMargin=18)
    
    # Create a list to hold the PDF content
    story = []
    
    # Get the style sheet
    styles = getSampleStyleSheet()
    
    # Add a title
    title = Paragraph("Neutral Analysis", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Add the analysis text
    para_style = styles['Normal']
    paragraphs = analysis.split('\n')
    for para in paragraphs:
        if para.strip():  # Only add non-empty paragraphs
            story.append(Paragraph(para, para_style))
            story.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(story)
    
    # Get the value of the BytesIO buffer
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def last_page(analysis):
    """
    Creates the last page displaying the analysis with PDF download option.
    
    Args:
        analysis (str): The analysis to be displayed
    """
    st.title("Analysis Results")
    
    # Display analysis
    st.write("Analysis Output:")
    st.write(analysis)
    
    # PDF Download Button
    pdf_button = st.download_button(
        label="Download Analysis as PDF",
        data=create_analysis_pdf(analysis),
        file_name="Neutral_Analysis.pdf",
        mime="application/pdf"
    )
    
    # Optional: Add a button to go back to first page
    if st.button("Back to Upload"):
        st.session_state.page = 'upload'
        st.rerun()


def send_to_ai(cv, decision):

    user_req = f'''Turn the text delimited by triple backticks into the following columns:
    S.No,Age,Accessibility,EdLevel,Employment,Gender,MentalHealth,MainBranch,YearsCode,YearsCodePro,Country,PreviousSalary,HaveWorkedWith,ComputerSkills,Employed,Age_Category,Is_Employed,Skills_List,Skills_Count,Education_Level,Gender_Category,Previous_Salary,Years_Coding,Years_Professional_Coding
    ```{cv}```
    RESPOND IN ONLY CSV VALUE - NO ADDITIONAL TEXT, ONLY THE VALUES IN COMMA SEPARATED FORMAT, DO NOT INCLUDE THE COLUMN NAMES EITHER 
    '''

    ai = AI(SYSTEM_PROMPT)
    new_columns = ai.generate_response(user_req)
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

    return document


def file_to_text(uploaded_file):
    """
    Converts an uploaded file (PDF, DOCX, or TXT) to text.
    
    Args:
        uploaded_file (UploadedFile): Streamlit uploaded file object
    
    Returns:
        str: The extracted text from the file
    
    Raises:
        ValueError: If an unsupported file type is uploaded
    """
    if uploaded_file is None:
        return ""
    
    # Determine file type based on file name
    filename = uploaded_file.name.lower()
    
    try:
        # PDF file handling
        if filename.endswith('.pdf'):
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            
            # Initialize an empty string to store the text
            full_text = ''
            
            # Extract text from each page
            for page in pdf_reader.pages:
                # Extract text from the current page and append to full_text
                full_text += page.extract_text() + '\n'
            
            return full_text.strip()
        
        # DOCX file handling
        elif filename.endswith('.docx'):
            # Read the docx file
            doc = docx.Document(uploaded_file)
            
            # Extract text from all paragraphs
            full_text = '\n'.join([para.text for para in doc.paragraphs])
            
            return full_text.strip()
        
        # TXT file handling
        elif filename.endswith('.txt'):
            # Read text files directly
            return uploaded_file.getvalue().decode('utf-8').strip()
        
        else:
            # Unsupported file type
            raise ValueError(f"Unsupported file type: {filename}")
    
    except Exception as e:
        st.error(f"Error processing file {filename}: {str(e)}")
        return ""


def main():
    # Initialize session state for page navigation and file contents
    if 'page' not in st.session_state:
        st.session_state.page = 'upload'
    
    # Routing logic
    if st.session_state.page == 'upload':
        results = first_page()
        # Store the results in session state
        st.session_state.cv = results[0]
        st.session_state.decision = results[1]
    elif st.session_state.page == 'analysis':
        # Retrieve stored CV and decision from session state
        cv = st.session_state.get('cv', '')
        decision = st.session_state.get('decision', '')
        
        print("BEFORE SENDING TO CV \n\n\n", cv)
        print("BEFORE SENDING TO AI DECISION \n\n\n", decision)
        
        analysis = send_to_ai(cv, decision)
        last_page(analysis)

        
# Run the main function
if __name__ == "__main__":
    main()