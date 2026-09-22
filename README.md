# 🤖 AI Software Engineer Assistant

> **College Project | Final Year / Mini Project Submission**
> **Institute:** [Arts,commeres & science college, Arvi]
> **Department:** Masters of Science / Computer Science
> **Academic Year:** 2026–2027

---

## 📌 Project Overview

**Problem Statement:**
Developers waste significant time trying to understand unfamiliar codebases — reading through hundreds of files, figuring out architecture, spotting bugs, and writing documentation manually. This slows down onboarding, code reviews, and collaboration.

**Our Solution:**
An AI-powered Software Engineer Assistant that takes a GitHub repository as input, automatically analyzes the entire codebase, and provides developers with instant insights — architecture diagrams, module explanations, duplicate code detection, security issues, performance suggestions, and auto-generated API documentation.

---

## 🎯 Objectives

- Reduce the time developers spend understanding new codebases
- Auto-generate architecture diagrams from source code
- Detect code quality issues (duplicates, security vulnerabilities)
- Suggest performance improvements using AI
- Auto-generate API documentation
- Allow developers to ask natural language questions about the codebase

---

## ⚙️ How It Works

```
User uploads GitHub repo URL
        ↓
AI clones & reads all files
        ↓
Parses code structure (AST / file tree)
        ↓
Sends to LLM (GPT / Gemini / open-source model)
        ↓
Returns: Diagrams | Explanations | Issues | Docs
        ↓
User can ask follow-up questions (Chat Interface)
```

---

## 🧩 Core Features

| Feature | Description |
|---|---|
| 📂 GitHub Repo Upload | Paste a public GitHub URL; system clones and processes it |
| 🗺️ Architecture Diagram | Auto-generates a visual diagram of the project structure |
| 📖 Module Explanation | AI explains every folder/file and what it does |
| 🔁 Duplicate Code Finder | Detects repeated code blocks across files |
| 🔐 Security Issue Detector | Flags hardcoded secrets, SQL injections, etc. |
| ⚡ Performance Suggestions | Recommends optimizations (N+1 queries, unused imports, etc.) |
| 📄 API Docs Generator | Automatically creates documentation for all API endpoints |
| 💬 Q&A Chat Interface | Ask questions like *"Where is authentication implemented?"* |

---

## 🛠️ Tech Stack

### Frontend
- **React.js** — UI for uploading repo, viewing results, chatting
- **Tailwind CSS** — Styling
- **Mermaid.js / D3.js** — Rendering architecture diagrams

### Backend
- **Python (FastAPI / Flask)** — REST API server
- **GitPython** — For cloning GitHub repositories
- **AST (Abstract Syntax Tree) Parser** — Code structure analysis

### AI / LLM Layer
- **OpenAI GPT-4 API** or **Google Gemini API** (or free alternative: **Ollama + CodeLlama**)
- **LangChain** — For chaining AI prompts and managing context
- **FAISS / ChromaDB** — Vector database for storing code embeddings (enables Q&A)

### Other Tools
- **GitHub API** — Fetching repository metadata
- **Docker** — Containerization for easy deployment

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────┐
│                  Frontend (React)            │
│   [Repo Input] [Diagram View] [Chat Box]     │
└──────────────────┬──────────────────────────┘
                   │ HTTP / REST
┌──────────────────▼──────────────────────────┐
│              Backend (FastAPI)               │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │ Git Clone│  │ AST Parse│  │ Doc Gen   │  │
│  └──────────┘  └──────────┘  └───────────┘  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│            AI / LLM Layer                   │
│  ┌──────────────┐   ┌─────────────────────┐ │
│  │ GPT / Gemini │   │ Vector DB (ChromaDB) │ │
│  │  (Analysis)  │   │  (Code Embeddings)  │ │
│  └──────────────┘   └─────────────────────┘ │
└─────────────────────────────────────────────┘
```

---

## 📋 Implementation Plan (Phase-wise)

### ✅ Phase 1 — Setup & Research (Week 1–2)
- [ ] Finalize tech stack
- [ ] Set up GitHub repo for the project itself
- [ ] Create basic React frontend skeleton
- [ ] Set up Python FastAPI backend
- [ ] Test GitHub repo cloning via `GitPython`
- [ ] Get API keys (OpenAI or Gemini)

### ✅ Phase 2 — Core Backend (Week 3–4)
- [ ] Build GitHub URL input + clone logic
- [ ] Implement file tree parser (list all files/folders)
- [ ] Build AST-based code parser for Python/JS files
- [ ] Send parsed code to LLM for module explanations
- [ ] Return structured JSON response to frontend

### ✅ Phase 3 — AI Features (Week 5–6)
- [ ] Integrate LangChain for prompt chaining
- [ ] Build code embedding pipeline → store in ChromaDB
- [ ] Implement duplicate code detection logic
- [ ] Implement security issue scanner (regex + LLM)
- [ ] Implement performance suggestion module

### ✅ Phase 4 — Frontend Development (Week 7–8)
- [ ] Build repo URL input page
- [ ] Build results dashboard (modules, issues, suggestions)
- [ ] Integrate Mermaid.js for architecture diagram rendering
- [ ] Build Q&A chat interface (connect to vector DB)
- [ ] Build API documentation display page

### ✅ Phase 5 — Integration & Testing (Week 9–10)
- [ ] Connect frontend ↔ backend fully
- [ ] Test with 3–5 real open-source GitHub repositories
- [ ] Fix bugs, improve prompts for better AI output
- [ ] Performance testing (how fast can it analyze a 100-file repo?)

### ✅ Phase 6 — Documentation & Submission (Week 11–12)
- [ ] Write full project report
- [ ] Prepare presentation slides (PPT)
- [ ] Record demo video
- [ ] Final code cleanup and submission

---

## 📁 Folder Structure (Planned)

```
ai-software-assistant/
│
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Main pages (Home, Dashboard, Chat)
│   │   └── App.jsx
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── routes/           # API routes
│   │   ├── services/         # Business logic (clone, parse, AI)
│   │   └── models/           # Data models
│   ├── requirements.txt
│   └── Dockerfile
│
├── ai/
│   ├── embeddings.py         # Code embedding logic
│   ├── analyzer.py           # LLM analysis calls
│   └── prompts/              # Prompt templates
│
├── docs/
│   ├── project_report.pdf
│   └── presentation.pptx
│
└── README.md
```

---

## 👨‍💻 Team & Roles

| Role | Responsibility |
|---|---|
| Frontend Developer | React UI, diagram rendering, chat interface |
| Backend Developer | FastAPI server, GitHub cloning, file parsing |
| AI/ML Developer | LLM integration, embeddings, prompt engineering |
| Tester / Docs | Testing, report writing, presentation |

> *(Assign your team members' names here)*

---

## 🚀 How to Run (Local Setup)

```bash
# 1. Clone the project
git clone https://github.com/your-username/ai-software-assistant.git
cd ai-software-assistant

# 2. Backend setup
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 3. Frontend setup
cd ../frontend
npm install
npm run dev

# 4. Add your API keys in .env
OPENAI_API_KEY=your_key_here
# OR
GEMINI_API_KEY=your_key_here
```

---

## 📊 Expected Output (Demo)

When a user pastes a GitHub URL like `https://github.com/facebook/react`:

1. **Architecture Diagram** — Shows folder structure visually
2. **Module Summary** — *"The `packages/react` folder contains the core React runtime..."*
3. **Security Report** — *"No hardcoded secrets found. 2 potential XSS risks detected."*
4. **Duplicate Code** — *"3 duplicate utility functions found across 5 files."*
5. **Performance Tips** — *"Consider lazy-loading components in `src/components/Router.js`"*
6. **API Docs** — Auto-generated markdown docs for all endpoints
7. **Chat** — User asks: *"Where is state management handled?"* → AI responds with file + line references

---

## 🏆 Why This Project?

- Solves a **real developer problem** (onboarding to new codebases)
- Uses **cutting-edge AI/LLM technology** (relevant and impressive for college)
- Covers **full-stack development** (frontend + backend + AI)
- Has a clear **demo-able output** (diagrams, docs, chat)
- Scalable — can be extended post-college into a real product

---

## 📚 References

- [OpenAI API Docs](https://platform.openai.com/docs)
- [Google Gemini API](https://ai.google.dev/)
- [LangChain Documentation](https://docs.langchain.com/)
- [ChromaDB Vector Store](https://docs.trychroma.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Mermaid.js Diagrams](https://mermaid.js.org/)
- [GitPython Library](https://gitpython.readthedocs.io/)

---

## 📝 License

This project is submitted for academic purposes at [Arts,commeres & Science college, Arvi].
All AI API usage is for educational and non-commercial use only.

---

*Made with ❤️ by [Janhavi Bhalchandra Bodakhe] | [Arts,commers & Science college, Arvi] | 2026–2027*
