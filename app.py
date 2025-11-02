from flask import Flask, request, render_template, jsonify
from docx import Document
import os

# try to import textract; it's optional on the Free plan
try:
    import textract  # noqa
except Exception:
    textract = None

from hf_inference import summarize_text  # NEW

app = Flask(__name__, static_folder="static", template_folder="template")

def extract_text(file_storage):
    filename = file_storage.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext == '.docx':
        doc = Document(file_storage)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    elif ext == '.doc':
        if not textract:
            raise RuntimeError(".doc files require textract/system deps. Use Docker deploy (see instructions) or upload .docx.")
        os.makedirs("temp", exist_ok=True)
        file_path = os.path.join("temp", filename)
        file_storage.save(file_path)
        try:
            text = textract.process(file_path).decode("utf-8", errors="ignore")
        finally:
            try:
                os.remove(file_path)
            except Exception:
                pass
        return text

    raise RuntimeError("Unsupported file type. Upload a .docx (or .doc with Docker deploy).")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        text = extract_text(file)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text to summarize"}), 400
    try:
        summary = summarize_text(text, max_length=200, min_length=60)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)