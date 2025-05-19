# 📝 Summarize – Document Summarization Web App

Summarize is a simple and powerful web app that allows users to upload `.docx` or `.doc` files and get concise summaries using state-of-the-art natural language processing.

Built with:
- ⚙️ Python + Flask
- 🤗 Hugging Face Transformers (`facebook/bart-large-cnn`)
- 🧠 Text extraction via `python-docx` and `textract`

## 🚀 Features

- Upload `.docx` or `.doc` files
- Extract and display full text from documents
- Generate high-quality summaries using BART model
- Clean and responsive UI
- Spinner and progress bar for better UX

## 📸 Demo
![image](https://github.com/user-attachments/assets/6e4df41b-353e-4302-b9ab-c063f2208c14)


Upload FIle doc or docx
![image](https://github.com/user-attachments/assets/84fe57c2-3f2b-4bb4-b805-f36392fa2df2)

![image](https://github.com/user-attachments/assets/c557591a-924c-405b-8fd4-1683bd8c52cd)

CLick Summarize
wait for loading to finish
![image](https://github.com/user-attachments/assets/ab724396-8f42-4a25-abd0-d63fbd43c14c)


Summarize Text
![image](https://github.com/user-attachments/assets/7df5714a-3dca-45f9-9f2b-2d670856436e)




![Demo Screenshot](screenshot.png) <!-- Optional: Add a screenshot of your app -->

## 📂 Folder Structure

Summarize/ <br>
├── app.py # Flask backend <br>
├── requirements.txt # Python dependencies <br>
├── template/ <br>
│ └── index.html # Frontend HTML <br>
├── static/ <br>
│ ├── styles.css # Custom styles <br>
│ └── main.js # JavaScript logic <br>



## 🧪 Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask
- **ML Model:** `facebook/bart-large-cnn` from Hugging Face
- **Text Extraction:** `python-docx`, `textract`

## 🧰 Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/summarize.git
   cd summarize

Create a virtual environment and activate it:
'''bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

Install dependencies:
'''bash
pip install -r requirements.txt



Run the Flask app:

python app.py

Open your browser at http://localhost:5000.
