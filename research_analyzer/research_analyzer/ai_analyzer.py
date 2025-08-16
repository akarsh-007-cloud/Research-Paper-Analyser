# ai_analyzer.py
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    print(f"Error configuring Google AI. Make sure you have a GOOGLE_API_KEY in your .env file. Details: {e}")
    exit()


def analyze_paper_with_ai(paper_text: str) -> dict:
    """
    Analyzes the text of a research paper using Google's Gemini model to extract metadata and summarize.

    Args:
        paper_text: The full text of the research paper.

    Returns:
        A dictionary containing the structured data, or None if an error occurs.
    """
    # The prompt remains the same. It's universal and works great with Gemini.
    prompt = f"""
    You are an expert research assistant. Your task is to analyze the following research paper text and extract key information. 
    Please provide the output in a clean JSON format. The JSON object should have the following keys:
    - "title": The main title of the paper.
    - "authors": A list of all author names.
    - "publication_info": A string describing where and when it was published (e.g., "Published in Nature, Vol 589, January 2021" or "Appeared in NeurIPS 2020 Conference").
    - "abstract": A concise summary of the paper's abstract.
    - "key_findings": A bullet-point list (as a single string with newline characters '\\n') summarizing the most important findings and contributions of the paper.

    Here is the text of the research paper:
    ---
    {paper_text[:20000]} 
    ---
    
    Please provide ONLY the JSON object as a response. Do not include any other text or markdown formatting like ```json.
    """
    # We truncate the text to stay within reasonable limits.

    try:
        print("Sending request to Gemini model. This may take a moment...")
        # We'll use the gemini-1.5-flash model, which is fast, capable, and free.
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # The API call to generate content
        response = model.generate_content(prompt)
        
        response_content = response.text
        print("Gemini response received.")

        # Clean up the response just in case it includes markdown backticks
        if response_content.startswith("```json"):
            response_content = response_content[7:-4].strip()
        
        # Parse the JSON string into a Python dictionary
        analysis_result = json.loads(response_content)
        return analysis_result

    except Exception as e:
        print(f"An error occurred during AI analysis with Gemini: {e}")
        # The Gemini response object has more details on errors if it fails to generate
        if 'response' in locals() and response.prompt_feedback:
            print("Prompt Feedback:", response.prompt_feedback)
        return None

# The testing part of the script remains the same
if __name__ == '__main__':
    from pdf_processor import extract_text_from_pdf

    test_pdf_path = r'C:\Users\akars\Downloads\research_analyzer\research_analyzer\sample_paper.pdf'
    text = extract_text_from_pdf(test_pdf_path)
    if text:
        analysis = analyze_paper_with_ai(text)
        if analysis:
            print("\n--- AI Analysis Result (from Gemini) ---")
            print(json.dumps(analysis, indent=4))