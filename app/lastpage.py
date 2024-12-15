import streamlit as st
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter




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


if __name__ == '__main__':
    final_analysis('look at me im an analysis')