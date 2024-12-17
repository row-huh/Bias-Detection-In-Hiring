import os
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Add the project root to the Python path if necessary
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import necessary functions from the model (assuming these are in the model folder)
from model.utility import *  # Assuming utility.py exists
from model.genai import *  # Assuming genai.py exists

# Page Config
st.set_page_config(layout="wide", page_title="Neutral AI Dashboard")

# Load external CSS
with open("static/style.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# Load external HTML template
with open("templates/template.html") as html_file:
    st.markdown(html_file.read(), unsafe_allow_html=True)

# Title and Description
st.title("Neutral AI Project Dashboard")
st.write("A beginner-friendly dashboard for visualizing and interacting with the Neutral AI project.")

# Sidebar Navigation
st.sidebar.header("Navigation")
options = ["Overview", "Data Visualization", "Metrics and Map", "Final Analysis"]
choice = st.sidebar.radio("Select a page:", options)

# Example Data
data = {
    "State": ["California", "Texas", "Florida", "New York", "Illinois"],
    "Population": [39538223, 29145505, 21538187, 20201249, 12812508],
    "Gain/Loss": [200000, 150000, -50000, -300000, -100000]
}
df = pd.DataFrame(data)

# Function to create map
def create_map():
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    for _, row in df.iterrows():
        folium.Marker(
            location=[37 + (row['Population'] % 10)/10, -95 + (row['Population'] % 10)/10],
            popup=f"{row['State']}: {row['Population']:,}",
            icon=folium.Icon(color="blue" if row['Gain/Loss'] > 0 else "red")
        ).add_to(m)
    return m

# Function for the file upload and first analysis (this is your first_page logic)
def first_page():
    UPLOAD_DIR = "uploads"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    uploaded_file_1 = st.file_uploader("Step 1: Upload Your CV (PDF format only)", type="pdf")
    uploaded_file_2 = st.file_uploader("Step 2: Upload the Company's Reason for Not Hiring (PDF format only)", type="pdf")

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

    if st.button("Start Bias Analysis"):
        if uploaded_file_1 and uploaded_file_2:
            st.success("Files uploaded and saved successfully! Starting analysis...", icon="📊")
            analysis_result = send_to_ai(file_path_1, file_path_2)
            return analysis_result
        else:
            st.error("Please upload both files before proceeding.")
    return None

# Function for displaying the final analysis result (this is your final_analysis logic)
def final_analysis(analysis: str):
    st.title("Detecting Biases in Hiring")
    st.header("Neutral's Analysis Result")
    st.markdown(f"""
        <div style="background-color: #222; color: #ddd; padding: 15px; border-radius: 5px;">
            <p style="font-size: 16px;">{analysis}</p>
        </div>
    """, unsafe_allow_html=True)

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
            if y < 50:
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

# Function to send files to AI for analysis (your send_to_ai function)
def send_to_ai(cv_path, decision_path):
    cv = pdf_to_text(cv_path)
    decision = pdf_to_text(decision_path)
    user_req = f'''Turn the text delimited by triple backticks into the following columns:
    S.No,Age,Accessibility,EdLevel,Employment,Gender,MentalHealth,MainBranch,YearsCode,YearsCodePro,Country,PreviousSalary,HaveWorkedWith,ComputerSkills,Employed,Age_Category,Is_Employed,Skills_List,Skills_Count,Education_Level,Gender_Category,Previous_Salary,Years_Coding,Years_Professional_Coding
    ```{cv}```
    RESPOND IN ONLY CSV VALUE - NO ADDITIONAL TEXT, ONLY THE VALUES IN COMMA SEPARATED FORMAT, DO NOT INCLUDE THE COLUMN NAMES EITHER
    '''
    ai = AI(SYSTEM_PROMPT)
    new_columns = ai.generate_response(user_req)
    ml_decision = 'BIASED'
    new_prompt = f""" 
    CV (delimited by triple backticks): ```{cv}```,
    Decision (delimited by double backticks): ``{decision}``,
    Expert's prediction: {ml_decision}
    Write 500 words explaining why the decision is biased or justified.
    """
    document = ai.generate_response(new_prompt)
    return document

# Main application flow
if choice == "Overview":
    analysis_result = first_page()  # This is your first page logic for file upload and analysis
    if analysis_result:
        st.session_state.analysis_result = analysis_result  # Store the result in session state

elif choice == "Data Visualization":
    st.subheader("Data Visualization")
    st.write("### Population Gain/Loss by State")
    fig = px.bar(df, x="State", y="Gain/Loss", color="Gain/Loss", title="State Gain/Loss Overview")
    st.plotly_chart(fig, use_container_width=True)
    st.write("### Detailed Table")
    st.dataframe(df)

elif choice == "Metrics and Map":
    st.subheader("Key Metrics and Map")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Population", f"{df['Population'].sum():,}")
    col2.metric("Total Gain", f"{df[df['Gain/Loss'] > 0]['Gain/Loss'].sum():,}")
    col3.metric("Total Loss", f"{df[df['Gain/Loss'] < 0]['Gain/Loss'].sum():,}")
    st.write("### Population Map")
    folium_static(create_map())

elif choice == "Final Analysis":
    if 'analysis_result' in st.session_state:
        final_analysis(st.session_state.analysis_result)  # Display the analysis result

# Footer
st.write("---")
st.write("Built with ❤️ using Streamlit and Plotly.")
