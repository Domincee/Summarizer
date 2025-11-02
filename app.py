from flask import Flask, request, render_template, jsonify
from docx import Document
import os

# Optional .doc support via textract (only works if you deploy with Docker + system deps)
try:
    import textract  # noqa
except Exception:
    textract = None

from summarizer_extractive import summarize_extractive  # << use local summarizer

app = Flask(__name__, static_folder="static", template_folder="template")

def extract_text(file_storage):
    filename = file_storage.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".docx":
        doc = Document(file_storage.stream)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    if ext == ".doc":
        if not textract:
            raise RuntimeError(".doc requires textract (deploy with Docker) or upload a .docx instead.")
        os.makedirs("temp", exist_ok=True)
        path = os.path.join("temp", filename)
        file_storage.save(path)
        try:
            return textract.process(path).decode("utf-8", errors="ignore")
        finally:
            try: os.remove(path)
            except Exception: pass

    raise RuntimeError("Unsupported file type. Upload a .docx (or .doc with Docker).")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        text = extract_text(f)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json() or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "No text to summarize"}), 400
    try:
        summary = summarize_extractive(text)  # local, free
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)