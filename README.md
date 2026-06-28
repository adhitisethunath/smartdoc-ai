# 📄 SmartDoc AI — Intelligent Document Summarizer

SmartDoc AI is a web application that uses Google's Gemini large language model to turn any text-based PDF into a clean, structured summary — complete with key points, keywords, action items, flashcards, and FAQs.

Built with **Python**, **Streamlit**, and the **Gemini API**.

---

## 🚀 Live Demo

> _Add your deployed Streamlit Cloud link here after deployment, e.g._
> https://smartdoc-ai-adhitisethunath.streamlit.app

---

## 🧩 Problem Statement

Students, researchers, and professionals routinely deal with long PDFs — research papers, reports, contracts, lecture notes — but rarely have time to read every page closely. Manually extracting the key ideas, action items, and important terms is slow and error-prone.

## 🎯 Objective

To build an AI-powered tool that automatically reads a PDF and generates a structured, easy-to-digest breakdown of its contents in seconds, saving the reader significant time while preserving the document's important information.

## 🌍 Real-World Applications

- **Students** — summarizing lecture notes, textbooks, and research papers before exams
- **Professionals** — quickly digesting reports, meeting minutes, or contracts
- **Researchers** — extracting key findings and action items from papers
- **Legal/HR teams** — scanning policies or agreements for key clauses and obligations

## ✨ Features

- 📤 Upload any text-based PDF
- 📝 AI-generated concise summary
- 🔑 Key points extraction
- 🏷️ Keyword/topic tagging
- ✅ Action item detection
- 🎓 Auto-generated flashcards for studying
- ❓ Auto-generated FAQs
- ⬇️ Downloadable summary report (.txt)
- 🛡️ Robust error handling (corrupt, empty, or oversized PDFs; API/network failures)
- 🎨 Clean, tabbed, professional Streamlit UI

## 🔮 Future Enhancements

See the [Improvements](#-future-improvements) section below for 15+ advanced features planned, including OCR support, multi-language summarization, and chat-with-PDF.

---

## 🛠️ Tech Stack

| Layer            | Technology                          |
|-------------------|--------------------------------------|
| Frontend/UI       | Streamlit                            |
| AI/LLM            | Google Gemini API (`gemini-1.5-flash`) |
| PDF Processing    | PyMuPDF (fitz)                       |
| Language          | Python 3.10+                         |
| Config Management | python-dotenv                        |
| Deployment        | Streamlit Community Cloud            |

---

## 📁 Project Structure

```
smartdoc-ai/
│
├── app.py                      # Main Streamlit app (UI layer only)
├── requirements.txt            # Python dependencies
├── .env.example                # Template for environment variables
├── .gitignore                  # Files Git should ignore
├── README.md                   # Project documentation (this file)
├── LICENSE                     # MIT License
│
├── .streamlit/
│   └── secrets.toml.example    # Template for Streamlit Cloud secrets
│
├── src/                        # Core application logic (modular)
│   ├── __init__.py
│   ├── pdf_extractor.py        # PDF text extraction + validation
│   ├── gemini_client.py        # Gemini API integration
│   ├── prompts.py              # Prompt engineering templates
│   └── utils.py                # Helper functions (formatting, etc.)
│
└── assets/                     # Screenshots, logo, demo images
```

---

## ⚙️ Installation & Setup

### Prerequisites

| Tool | Purpose | Link |
|------|---------|------|
| Python 3.10+ | Runtime | https://www.python.org/downloads/ |
| VS Code | Code editor | https://code.visualstudio.com/ |
| Git | Version control | https://git-scm.com/downloads |
| Gemini API Key | AI summarization | https://aistudio.google.com/app/apikey |

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/smartdoc-ai.git
cd smartdoc-ai

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up your API key
cp .env.example .env
# Open .env and paste your real Gemini API key

# 6. Run the app
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## 🔑 Getting a Gemini API Key

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with a Google account
3. Click **Create API Key**
4. Copy the key into your `.env` file as `GEMINI_API_KEY=your_key_here`

The free tier is sufficient for development and demos.

---

## 🧪 Error Handling

SmartDoc AI gracefully handles:
- Empty or non-text (scanned/image-only) PDFs
- Corrupted or invalid PDF files
- Oversized PDFs (configurable page/size limits)
- Gemini API failures (bad key, quota limits, network issues)
- Malformed AI responses

---

## ☁️ Deployment (Streamlit Community Cloud)

1. Push this repo to GitHub (public or private)
2. Go to https://share.streamlit.io
3. Click **New app**, select your repo, branch, and `app.py` as the entry point
4. Under **Advanced settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_real_key_here"
   ```
5. Click **Deploy** — your app will be live at `https://<your-app-name>.streamlit.app`

---

## 🔮 Future Improvements

- Multi-language summarization
- OCR support for scanned PDFs (via Tesseract)
- Chat-with-PDF (conversational Q&A over the document)
- Semantic search across uploaded documents
- Voice/audio summary generation (text-to-speech)
- Export results to Word/PDF
- Highlight important sentences directly in the PDF viewer
- User authentication and summary history
- Support for DOCX, TXT, and URL inputs
- Batch processing of multiple PDFs
- Comparison mode between two documents

---

## 📜 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 🙋 Author

**Your Name**
[GitHub](https://github.com/your-username) • [LinkedIn](https://linkedin.com/in/your-profile)