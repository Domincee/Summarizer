# 📝 Summarize — Document Summarization Web App (Free)

A simple Flask web app to **extract text from DOC/DOCX files** and generate a **concise summary**.  
Built to run **100% free** on Render’s Free Plan — **no external ML APIs, no GPU, no billing.**

---

## ✨ Features

- 📂 Upload `.docx` (and `.doc` if deployed with Docker + textract)
- 🖱️ Drag & drop upload zone or click to browse
- 🧠 Text extraction with `python-docx`
- ⚡ Fast, extractive summaries using **Sumy (LexRank)**
- ⏳ Progress bar and typewriter effect while summarizing
- 💻 Modern, responsive UI
- 🆓 Fully compatible with **Render’s Free plan**

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Flask |
| **Summarization** | Sumy (LexRank), NLTK |
| **Text Extraction** | python-docx (.docx) <br> Optional textract (.doc) |
| **Frontend** | HTML, CSS, JavaScript |

---

## 📂 Folder Structure
-
├── app.py <br>
├── summarizer_extractive.py <br>
├── requirements.txt <br>
├── template/ <br>
│ └── index.html <br>
├── static/<br>
│ ├── styles.css <br>
│ └── main.js<br>
└── (optional) Dockerfile # only if you need .doc support<br>



---

## 🚀 Local Development

### **Prerequisites**
- Python **3.10+** (3.11 recommended)

### **Setup Steps**

```bash
# Clone repo
git clone https://github.com/yourusername/summarizer.git
cd summarizer

# Create virtual environment
python -m venv .venv

# Activate venv
# Windows
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
python app.py
```

🌐 Then open your browser and visit:
http://localhost:5000


🧩 Notes
- NLTK punkt data is auto-downloaded on first summarize call.
- If you want to pre-fetch locally:
  
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```


🌐 Deploy on Render (Free)
Go to Render Dashboard
 → New → Web Service
- Connect your GitHub repo

- Choose Environment: Python

- Set the following commands:

- Build command:
```bash
- pip install -r requirements.txt
```

```bash
gunicorn -w 1 -k gthread --threads 8 --timeout 120 -b 0.0.0.0:$PORT app:app
```
