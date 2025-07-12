import os
import subprocess
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
OUTPUT_FOLDER = '/tmp/output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files.get('pdf_file')

    # ✅ Fix 1: Handle .PDF and other cases safely
    if not file or not file.filename.lower().endswith('.pdf'):
        return "Invalid file", 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_filename = os.path.splitext(filename)[0] + '.docx'
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    file.save(input_path)

    try:
        # ✅ Fix 2: Use more reliable DOCX filter
        result = subprocess.run([
            'libreoffice',
            '--headless',
            '--convert-to', 'docx:MS Word 2007 XML',
            '--outdir', OUTPUT_FOLDER,
            input_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        print("STDOUT:\n", result.stdout.decode())
        print("STDERR:\n", result.stderr.decode())

    except subprocess.CalledProcessError as e:
        return f"Conversion failed:<br><pre>{e.stderr.decode()}</pre>", 500

    if not os.path.exists(output_path):
        return f"Conversion failed: DOCX not created at {output_path}", 500

    return send_file(output_path, as_attachment=True)