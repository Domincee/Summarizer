from flask import Flask, request, render_template, jsonify
from docx import Document
import textract
from transformers import pipeline
import os


app = Flask(__name__, static_folder="static", template_folder="template")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text(file_storage):
    filename = file_storage.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext == '.docx':
        doc = Document(file_storage)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    elif ext == '.doc':
        os.makedirs("temp", exist_ok=True)
        file_path = os.path.join("temp", filename)
        file_storage.save(file_path)
        text = textract.process(file_path).decode("utf-8")
        os.remove(file_path)
        return text
    return None

@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if file:
        try:
            text = extract_text(file)
            return jsonify({"text": text})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "No file uploaded"}), 400

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "")
    if text:
        try:
            result = summarizer(text[:1024], max_length=100, min_length=30, do_sample=False)
            return jsonify({"summary": result[0]["summary_text"]})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "No text to summarize"}), 400

if __name__ == "__main__":
    app.debug = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=5200)