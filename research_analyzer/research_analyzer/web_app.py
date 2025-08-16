from flask import Flask, request, render_template, send_file
import os
from werkzeug.utils import secure_filename
from pdf_processor import extract_text_from_pdf
from ai_analyzer import analyze_paper_with_ai
from output_generator import save_as_docx


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['pdf']
        if pdf_file.filename == '':
            return "No selected file"

        filename = secure_filename(pdf_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        pdf_file.save(file_path)

        # Extract and analyze
        paper_text = extract_text_from_pdf(file_path)
        if not paper_text:
            return "Failed to extract text from PDF."

        analysis = analyze_paper_with_ai(paper_text)
        if not analysis:
            return "AI analysis failed."

        # Save DOCX
        docx_path = os.path.join(UPLOAD_FOLDER, filename.replace('.pdf', '_analysis.docx'))
        save_as_docx(analysis, docx_path)

        return render_template("result.html", data=analysis, docx_path=docx_path)

    return render_template("index.html")

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
