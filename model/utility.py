# this file contains helper functions

import PyPDF2


SYSTEM_PROMPT = 'say hello to everything'

def pdf_to_text(path):
    """
    Opens a PDF file and returns its text content.
    
    Args:
        path (str): The file path to the PDF document
    
    Returns:
        str: The extracted text from the PDF
    
    Raises:
        FileNotFoundError: If the PDF file cannot be found
        PyPDF2.errors.PdfReadError: If there's an issue reading the PDF
    """
    # Open the PDF file in read-binary mode
    with open(path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Initialize an empty string to store the text
        full_text = ''
        
        # Extract text from each page
        for page in pdf_reader.pages:
            # Extract text from the current page and append to full_text
            full_text += page.extract_text() + '\n'
        
        # Return the extracted text, stripping any leading/trailing whitespace
        return full_text.strip()