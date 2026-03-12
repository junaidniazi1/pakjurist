<div align="center">

# ⚖️ PakJurist
### AI-Powered Pakistan Legal Awareness System

*Pakistani law, made accessible for everyone.*

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Educational](https://img.shields.io/badge/Purpose-Educational%20Only-f59e0b?style=flat-square)]()

</div>

---

## 📽️ Demo

<div align="center">

https://github.com/user-attachments/assets/demo.mp4

> *Ask PakJurist about Pakistani law in English, Urdu, or Roman Urdu — with voice input and voice output.*

</div>

---

## 🧠 Why PakJurist?

Pakistani law is **complex, fragmented, and constantly changing.**

Legal information is scattered across hundreds of books, gazettes, and statutes — with amendments issued every month, inconsistent documentation, and no single reliable source for the average citizen. Most people have no practical way to access or understand the law that governs their daily lives.

**PakJurist was built to solve exactly that.**

### Why Google Gemini?

Because Pakistani law doesn't live in one place. It's spread across:

- 📖 The Constitution of Pakistan
- 📋 Pakistan Penal Code (PPC) & Criminal Procedure Code (CrPC)
- 🏛️ Provincial statutes & federal gazettes
- ⚖️ Court judgments & case law
- 📝 Amendments that change **every single month**

A traditional database or static knowledge base **cannot handle that complexity.** Gemini's large language model reasoning allows PakJurist to navigate this fragmented, inconsistent legal landscape intelligently — drawing connections across sources and presenting them in plain, accessible language.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🌐 **Multilingual** | Ask in English, اردو (Urdu), or Roman Urdu |
| 🤖 **AI Legal Q&A** | Powered by Google Gemini 2.5 Flash |
| 📄 **Document Analysis** | Upload PDFs, Word docs, or images for AI legal analysis |
| 🎤 **Voice Input** | Speech-to-Text via Google Speech Recognition |
| 🔊 **Voice Output** | Text-to-Speech via Coqui TTS (multilingual + voice cloning) |
| 💬 **Chat History** | Persistent session history with multi-session support |
| ⚡ **Quick Topics** | One-click shortcuts for the most common legal areas |
| 📊 **Session Stats** | Track your conversation history |

---

## 🏛️ Legal Coverage

```
📜 Constitution of Pakistan       ⚖️  Criminal Law (PPC / CrPC)
📋 Civil Law                      👨‍👩‍👧  Family Law
💼 Business & Commercial Law      🏠  Property Law
👷 Labor Law                      💰  Tax Law
```

---

## 🖥️ Tech Stack

```
Frontend        →  Streamlit
AI Model        →  Google Gemini 2.5 Flash
TTS Engine      →  Coqui TTS (coqui-tts fork)
STT Engine      →  Google Speech Recognition
PDF Parser      →  PyPDF2
DOCX Parser     →  python-docx
Image Support   →  Pillow
Database        →  SQLite (via custom Database class)
Language        →  Python 3.9+
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- A Google Gemini API key → [Get one free here](https://ai.google.dev)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pakjurist.git
cd pakjurist
```

### 2. Install Dependencies

```bash
pip install streamlit google-generativeai pillow PyPDF2 python-docx
pip install SpeechRecognition audio-recorder-streamlit
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install coqui-tts
```

> ⚠️ **Important:** Use `pip install coqui-tts` — do **NOT** use `pip install TTS` (that package is abandoned and broken on Windows).

### 3. Set Your API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Or export it as an environment variable:

```bash
# Windows
set GEMINI_API_KEY=your_gemini_api_key_here

# Linux / macOS
export GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

---

## 📁 Project Structure

```
pakjurist/
│
├── app.py              # Main Streamlit UI application
├── agent.py            # AI agent — Gemini, TTS, STT, document processing
├── database.py         # SQLite session & conversation history
├── requirements.txt    # Python dependencies
├── .env                # API keys (do not commit)
├── .gitignore
└── README.md
```

---

## 🌍 Language Support

PakJurist supports three languages out of the box:

| Language | Input | Voice Output (TTS) |
|---|---|---|
| English | ✅ | ✅ |
| اردو Urdu | ✅ | ✅ Native Urdu VITS model |
| Roman Urdu | ✅ | ✅ |

---

## 🔐 How It Stays Accurate

- **No hallucination policy** — Only references well-known, established provisions of Pakistani law
- **Uncertainty transparency** — If information cannot be verified, the system clearly states this
- **Source references** — Responses include links to official legal sources wherever possible
- **Scope-limited** — Questions unrelated to Pakistani law are gracefully declined

---

## ⚠️ Disclaimer

> PakJurist is for **educational and informational purposes only.**
> It is **not a lawyer** and does **not provide legal advice.**
> For specific legal matters, always consult a licensed Pakistani lawyer.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve PakJurist:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ for the people of Pakistan

**⚖️ PakJurist — Qanoon Sabke Liye**

*قانون سب کے لیے*

</div>
