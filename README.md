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

