import streamlit as st

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Neutral - Bias Detection",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Link the external CSS file
st.markdown(
    """
    <link rel="stylesheet" type="text/css" href="styles.css">
    """,
    unsafe_allow_html=True,
)

# Navigation Bar: Left and Right Aligned Options
st.markdown(
    """
    <header>
    <div class="navbar">
        <!-- Left-side Navigation Links -->
        <div class="left-side">
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="#" class="nav-link">Home</a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link">About</a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link">Services</a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link">Resume</a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link">Cover Letters</a>
                </li>
            </ul>
        </div></header>
    """,
    unsafe_allow_html=True,
)


# Header Section
st.markdown(
    """
    <div class="content-section">
        <center><h1 style="color: #4C6A92;">Neutral</h1></center>
        <center><h3 style="color: #6C8EBF;">Detecting Biases in Hiring </h3></center>
    </div>
    """,
    unsafe_allow_html=True,
)

# Input Section
st.markdown(
    """
    <div class="content-section">
        <h4 style="color: #4C6A92;">Upload Hiring Data:</h4>
        <p style="color: #6C8EBF;">Upload a CSV file containing candidate information and hiring decisions to analyze for potential biases.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file_1 = st.file_uploader("Step 1: Upload Your CV", type="pdf")
uploaded_file_2 = st.file_uploader("Step 2: Reason from Company on not being hired", type="pdf")

# Display uploaded files
if uploaded_file_1 is not None:
    st.image(uploaded_file_1, caption="Uploaded CV", use_column_width=True)

if uploaded_file_2 is not None:
    st.image(uploaded_file_2, caption="Uploaded Reason File", use_column_width=True)

# Analysis Button
if st.button("Analyze for Biases"):
    if uploaded_file_1 is not None and uploaded_file_2 is not None:
        st.success("Files uploaded successfully! Starting analysis...", icon="📊")
        # Placeholder for actual analysis functionality
        st.info("Analysis is under development. Stay tuned!", icon="🔄")
    else:
        st.error("Please upload both files before proceeding.", icon="⚠")

# Footer Section
st.markdown(
    """
    <div class="footer">
        <center><p>&copy; 2024 Neutral. All rights reserved.</p></center>
    </div>
    """,
    unsafe_allow_html=True,
)
