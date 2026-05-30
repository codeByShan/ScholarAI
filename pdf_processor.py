# We are importing the PyPDF2 library
# It is a library that helps us in reading and extracting the text from PDF files
import PyPDF2

# we are importing io library
# io library helps us handle file data in memory
# When the user uploads a PDF through streamlit it comes as bytes (raw data)
# io helps us in converting those bytes into a readable file format
import io


# This is the main function that will extract the text from PDF file 
# It takes one input : the uploaded PDF file
def extract_text_from_pdf(uploaded_file):
    # uploaded file comes from streamlit as raw bytes
    # PyPDF2 cannot read raw bytes directly
    # So we wrap it in io.BytesIO to make it readable
    # Think of it like putting the file in a proper folder so PyPDF2 can open it
    pdf_file = io.BytesIO(uploaded_file.read())

    # PdfReader is a class inside PyPDF2
    # It opens and reads the PDF file
    # We pass our pdf_file to it
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # We create an empty string to store all extracted text
    # We will keep adding text from each page to this variable
    extracted_text = ""

    # pdf_reader.pages gives us a list of all pages in the PDF
    # We loop through each page one by one
    for page in pdf_reader.pages:

        # page.extract_text() extracts all text from that single page
        # We add it to our extracted_text variable
        # \n adds a new line after each page so text is organized
        extracted_text += page.extract_text() + "\n"
    

    # After looping through all pages
    # extracted_text now contains all text from the entire PDF
    # We return it so other parts of our app can use it
    return extracted_text


# This is a helper function that gives us basic info about the PDF
# It takes the uploaded file as input
def get_pdf_info(uploaded_file):
    
    # Same as before — wrap bytes in BytesIO
    pdf_file = io.BytesIO(uploaded_file.read())
    
    # Open the PDF with PdfReader
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    # Get total number of pages
    # len(pdf_reader.pages) counts how many pages are in the PDF
    total_pages = len(pdf_reader.pages)
    
    # We return a dictionary with basic PDF information
    # Dictionary is like a labeled container with key value pairs
    return {
        "total_pages": total_pages,
    }
