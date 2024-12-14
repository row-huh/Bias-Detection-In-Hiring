import streamlit as st
from PyPDF2 import PdfWriter
from io import BytesIO

def final_analysis(analysis: str):
    """
    Displays the given analysis on a Streamlit page with the heading 'Neutral's Analysis Result' 
    and provides a button to download the analysis as a PDF.

    Parameters:
        analysis (str): The analysis text to display and download.
    """

    # Top header bar
    st.markdown(
        """
        <style>
            .header-bar {
                background-color: #008080; /* Teal color matching existing UI */
                padding: 10px;
                color: white;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
            }
            .download-button {
                background-color: #00cc66; /* Green button color matching existing UI */
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            .download-button:hover {
                background-color: #00994d; /* Darker green for hover effect */
            }
        </style>
        <div class="header-bar">Neutral</div>
        """,
        unsafe_allow_html=True,
    )

    # Page heading
    st.title("Detecting Biases in Hiring")

    # Subheading for the analysis result
    st.header("Neutral's Analysis Result")

    # Display the analysis text in a container
    st.markdown(
        f"""
        <div style="background-color: #222; color: #ddd; padding: 15px; border-radius: 5px;">
            <p style="font-size: 16px;">{analysis}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Helper function to generate a PDF
    def generate_pdf(content):
        pdf_writer = PdfWriter()
        pdf_stream = BytesIO()

        # Create a simple text-based PDF
        pdf_writer.add_blank_page(width=72 * 8.5, height=72 * 11)  # Letter size
        pdf_writer.add_text(content, x=50, y=700)  # Adding text to the page

        pdf_writer.write(pdf_stream)
        pdf_stream.seek(0)
        return pdf_stream

    # Button to download the analysis as PDF
    st.markdown(
        """
        <form action="#" method="get">
            <button class="download-button" type="button" onclick="window.location.href='/download'">📝 Download as PDF</button>
        </form>
        """,
        unsafe_allow_html=True,
    )

    # Generate PDF when the button is clicked
    if st.button("Generate PDF"):
        pdf_stream = generate_pdf(analysis)
        st.download_button(
            label="Download PDF",
            data=pdf_stream.getvalue(),
            file_name="analysis_result.pdf",
            mime="application/pdf",
        )



#TODO
# only implement one function
# it takes one document - call the document an 'analysis'
# it only prints the analysis on streamlit with a heading like 'Neutral's Analysis Result'
# It also has a button with the print logo upon clicking which the document is downloaded on the user's pc in a pdf format
# it is only one function - helper functions may be used to improve readability but the main logic must exist in only one function
# ensure that the newly generated streamlit page follows the existing ui (insert existing ui picture)