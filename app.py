import os
import subprocess
from flask import Flask, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return redirect('/')

    file = request.files['pdf_file']
    if file.filename == '' or not file.filename.lower().endswith('.pdf'):
        return redirect('/')

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_filename = os.path.splitext(filename)[0] + '.docx'
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    file.save(input_path)

    try:
        # Convert using LibreOffice
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "docx", "--outdir", OUTPUT_FOLDER, input_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        return f"Conversion failed: {e.stderr.decode()}", 500

    if not os.path.exists(output_path):
        return "Conversion failed: output file not found.", 500

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
