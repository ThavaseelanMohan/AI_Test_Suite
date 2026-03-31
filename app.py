from flask import Flask, render_template, request, jsonify, send_file
from utils.summarizer import summarize_brd
from utils.test_generator import generate_test_cases
from utils.reviewer import review_test_cases
from utils.file_reader import read_file
import os
import pandas as pd
from version import __version__  # Import project version

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("outputs", exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html', version=__version__)

@app.route('/summarize', methods=['POST'])
def summarize():
    file = request.files.get('brd_file')
    if not file:
        return jsonify({"error": "No file uploaded"})
    try:
        content = read_file(file)
        if isinstance(content, pd.DataFrame):
            text = " ".join(content.astype(str).apply(lambda row: " ".join(row), axis=1))
        else:
            text = content
        summary = summarize_brd(text)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/generate', methods=['POST'])
def generate():
    file = request.files.get('brd_file')
    if not file:
        return jsonify({'error': 'No file uploaded'})
    try:
        content = read_file(file)
        if isinstance(content, pd.DataFrame):
            text = " ".join(content.astype(str).apply(lambda row: " ".join(row), axis=1))
        else:
            text = content
        test_cases, csv_path = generate_test_cases(text)
        return jsonify({'test_cases': test_cases, 'csv_file': csv_path})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/review', methods=['POST'])
def review():
    dev_file = request.files.get('dev_file')
    qa_file = request.files.get('qa_file')
    if not dev_file or not qa_file:
        return jsonify({"error": "Both Dev and QA files are required"})
    try:
        dev_path = os.path.join(UPLOAD_FOLDER, dev_file.filename)
        qa_path = os.path.join(UPLOAD_FOLDER, qa_file.filename)
        dev_file.save(dev_path)
        qa_file.save(qa_path)

        dev_df = pd.read_csv(dev_path) if dev_path.endswith(".csv") else pd.read_excel(dev_path)
        qa_df = pd.read_csv(qa_path) if qa_path.endswith(".csv") else pd.read_excel(qa_path)

        dev_csv = os.path.join("outputs", "dev_temp.csv")
        qa_csv = os.path.join("outputs", "qa_temp.csv")
        dev_df.to_csv(dev_csv, index=False)
        qa_df.to_csv(qa_csv, index=False)

        result = review_test_cases(dev_csv, qa_csv)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)