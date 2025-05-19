# summarize_docx.py

from docx import Document
from transformers import pipeline

def extract_docx_text(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def write_to_html(summary, output_path="summary.html"):
    html_content = f"""
    <html>
        <head><title>Summary</title></head>
        <body>
            <h1>Document Summary</h1>
            <p>{summary}</p>
        </body>
    </html>
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your file
    text = extract_docx_text(docx_path)
    summary = summarize_text(text)
    write_to_html(summary)
    print("✅ Summary written to summary.html")
