# main.py
import argparse
import os
from pdf_processor import extract_text_from_pdf
from ai_analyzer import analyze_paper_with_ai
from output_generator import save_as_json, save_as_docx

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Analyze a research paper PDF and extract metadata.")
    parser.add_argument("pdf_path", type=str, help="The file path to the research paper PDF.")
    args = parser.parse_args()

    pdf_path = args.pdf_path

    # Check if the file exists
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' was not found.")
        return

    # --- Step 1: Extract text from the PDF ---
    paper_text = extract_text_from_pdf(pdf_path)
    if not paper_text:
        print("Could not extract text from the PDF. Exiting.")
        return

    # --- Step 2: Analyze the text with AI ---
    analysis_data = analyze_paper_with_ai(paper_text)
    if not analysis_data:
        print("AI analysis failed. Exiting.")
        return
        
    # --- Step 3: Generate output files ---
    # Create a base name for the output files from the input PDF name
    base_output_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # Define output paths
    json_output_path = f"{base_output_name}_analysis.json"
    docx_output_path = f"{base_output_name}_analysis.docx"

    # Save the results
    save_as_json(analysis_data, json_output_path)
    save_as_docx(analysis_data, docx_output_path)
    
    print("\n--- Project Finished Successfully! ---")
    print(f"Check the directory for your files: '{json_output_path}' and '{docx_output_path}'")

if __name__ == "__main__":
    main()