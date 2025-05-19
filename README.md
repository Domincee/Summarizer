

# 📝 Summarize – Document Summarization Web App
A simple Flask web application that allows users to upload .doc or .docx files, extract the text content, and generate a concise summary using a transformer-based model.


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
- Minimal, clean interface

Optionally share your local server using <a href="https://ngrok.com/"> ngrok </a>




## 📸 Demo
![image](https://github.com/user-attachments/assets/6e4df41b-353e-4302-b9ab-c063f2208c14)

<b>Upload FIle doc or docx </b>

![image](https://github.com/user-attachments/assets/84fe57c2-3f2b-4bb4-b805-f36392fa2df2)

![image](https://github.com/user-attachments/assets/c557591a-924c-405b-8fd4-1683bd8c52cd)

<b>CLick Summarize</b> <br>
<b>wait for loading to finish</b><br>

![image](https://github.com/user-attachments/assets/ab724396-8f42-4a25-abd0-d63fbd43c14c)

<bSummarized Text</b><br>

![image](https://github.com/user-attachments/assets/7df5714a-3dca-45f9-9f2b-2d670856436e)



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

2. Create a virtual environment and activate it:
 ```bash
 python -m venv venv
  ```
source venv/bin/activate <br> # or <br>
 ```bash
 venv\Scripts\activate
 ```
 on Windows

3.Install dependencies:<br>
```bash 
pip install -r requirements.txt 
```

4.Run the Flask app:
```bash 
python app.py
```
Open your browser at 
```bash 
http://localhost:5000.
```

🌐 Deployment <br>
This app can be deployed on:<br>

Hugging Face Spaces (recommended for ML apps)<br>

Render, Railway, Google Cloud Run, Replit (may require higher memory plans)<br>

🙌 Acknowledgements <br>
Hugging Face Transformers<br>

Python-Docx<br>

Textract<br>
