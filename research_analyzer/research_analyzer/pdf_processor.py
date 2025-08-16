# pdf_processor.py
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all text content from a given PDF file.

    Args:
        pdf_path: The file path to the PDF document.

    Returns:
        A single string containing all the text from the PDF.
    """
    try:
        document = fitz.open(pdf_path)
        full_text = ""
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            full_text += page.get_text() + "\n" # Add a newline between pages
        
        print(f"Successfully extracted text from {pdf_path}. Total characters: {len(full_text)}")
        return full_text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None

if __name__ == '__main__':
    # This is for testing the function directly
    # Make sure you have a PDF file named 'sample_paper.pdf' in your project folder
    test_pdf_path = r'C:\Users\akars\Downloads\research_analyzer\research_analyzer\sample_paper.pdf' 
    extracted_text = extract_text_from_pdf(test_pdf_path)
    if extracted_text:
        # Print the first 500 characters to check
        print("\n--- First 500 characters ---")
        print(extracted_text[:500])