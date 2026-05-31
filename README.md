# 🔬 ScholarAI — Intelligent Research Paper Assistant

> An AI powered web application that helps students and researchers understand research papers instantly using Google Gemini LLM and RAG architecture.

---

## 🚀 Live Demo

**[https://scholar-research-ai.streamlit.app](https://scholar-research-ai.streamlit.app)**

---

## 📌 What is ScholarAI?

Reading and understanding research papers is one of the most time consuming tasks for students and researchers. A single paper can take hours to fully comprehend.

**ScholarAI solves this by:**
- Instantly summarizing any research paper
- Extracting key insights and findings
- Generating proper academic citations
- Answering any question about the paper in natural language

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Paper Summary** | Automatically generates a comprehensive summary covering objective, methodology, findings and conclusion |
| 🔍 **Key Insights** | Extracts problem statement, proposed solution, dataset, results, limitations and future work |
| 📚 **Citation Generation** | Generates proper academic citations in APA, MLA and Chicago formats |
| 💬 **Q&A Chat** | Ask any question about the paper and get accurate context aware answers with conversation memory |

---

## 🧠 How It Works

ScholarAI is built on **RAG (Retrieval Augmented Generation)** architecture:

```
User uploads PDF
        ↓
PyPDF2 extracts text from PDF
        ↓
LangChain splits text into chunks
        ↓
HuggingFace converts chunks to embeddings
        ↓
FAISS stores embeddings in vector database
        ↓
User asks question / requests summary
        ↓
FAISS retrieves most relevant chunks
        ↓
Google Gemini LLM generates accurate answer
        ↓
Result displayed in Streamlit UI
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Streamlit** | Web application UI |
| **Google Gemini LLM** | Core language model for understanding and generating answers |
| **LangChain** | RAG pipeline orchestration |
| **FAISS** | Vector database for storing and searching embeddings |
| **HuggingFace** | Sentence embeddings model (all-MiniLM-L6-v2) |
| **PyPDF2** | PDF text extraction |
| **Python** | Core programming language |

---

## 📁 Project Structure

```
ScholarAI/
    ├── app.py              ← Main Streamlit web application
    ├── pdf_processor.py    ← PDF text extraction module
    ├── rag_pipeline.py     ← RAG pipeline and vector database
    ├── gemini_handler.py   ← Google Gemini LLM integration
    ├── requirements.txt    ← Project dependencies
    ├── .gitignore          ← Git ignore file
    └── README.md           ← Project documentation
```

---

## ⚙️ Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/codeByShan/ScholarAI.git
cd ScholarAI
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API key
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your free Gemini API key from [Google AI Studio](https://aistudio.google.com)

### 5. Run the app
```bash
streamlit run app.py
```

---

## 🌍 Deployment

This app is deployed on **Streamlit Cloud** for free.

To deploy your own version:
1. Fork this repository
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add `GEMINI_API_KEY` in Streamlit Secrets
5. Deploy!

---

## 📸 Screenshots

### Home Screen
Upload any research paper PDF to get started.

<img width="730" height="389" alt="image" src="https://github.com/user-attachments/assets/a88d2f12-f9e5-4950-b631-d23759635d94" />

### Paper Summary
Get a comprehensive summary covering all key aspects of the paper.

<img width="748" height="382" alt="image" src="https://github.com/user-attachments/assets/d95cf712-58b1-48b6-a7a4-0bdc7773c001" />

### Key Insights
Extract structured insights including problem, solution, dataset and results.

<img width="722" height="379" alt="image" src="https://github.com/user-attachments/assets/9ac443b2-6a3c-4f2c-82fb-fa5acd1cd128" />

### Academic Citations
Generate proper citations in APA, MLA and Chicago formats instantly.

<img width="695" height="332" alt="image" src="https://github.com/user-attachments/assets/054dae58-f442-42cf-9189-bf54e691979c" />

### Q&A Chat
Ask any question about the paper and get accurate answers with conversation memory.

![Uploading image.png…]()

---

## 🎯 Use Cases

- **Students** — Understand research papers quickly without reading every page
- **Researchers** — Extract key findings and insights efficiently
- **Academics** — Generate proper citations automatically
- **Professionals** — Stay updated with latest research in your field

---

## ⚠️ Limitations

- Works best with text based PDFs (not scanned images)
- Gemini free tier has rate limits — may show busy message during peak hours
- Summary is based on first 5000 characters of the paper
- Q&A answers are limited to content within the uploaded paper

---

## 🔮 Future Improvements

- [ ] Support for multiple PDF uploads simultaneously
- [ ] Search across 200M+ academic papers (like real ScholarAI)
- [ ] Export summary and insights as Word/PDF document
- [ ] Multilingual support for Urdu and other languages
- [ ] Study guide and flashcard generation

---

## 👨‍💻 Developer

**Zeeshan Ali** (codeByShan)

Aspiring AI Engineer

Built as Final Year Project for AI Bootcamp

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with ❤️ using Google Gemini, LangChain and Streamlit*
