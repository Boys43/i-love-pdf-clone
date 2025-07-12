import os
from flask import Flask, render_template, request, send_file, redirect, flash
from werkzeug.utils import secure_filename
from pdf2docx import Converter

# Flask setup
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flashing messages

# Directories
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Check if uploaded file is PDF
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        flash('No file part in the request.')
        return redirect('/')

    file = request.files['pdf_file']
    if file.filename == '':
        flash('No file selected.')
        return redirect('/')

    if not allowed_file(file.filename):
        flash('Only PDF files are allowed.')
        return redirect('/')

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    output_filename = filename.rsplit('.', 1)[0] + '.docx'
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    file.save(input_path)

    try:
        cv = Converter(input_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()
    except Exception as e:
        flash(f"Conversion failed: {str(e)}")
        return redirect('/')

    return send_file(output_path, as_attachment=True, download_name=output_filename, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
