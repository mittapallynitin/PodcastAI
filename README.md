# 🎙️ Podcast AI

**Podcast AI** is an AI-driven platform that converts research papers (e.g., from ArXiv) into podcast-like narratives. Key features include secure user authentication, automated PDF parsing, script generation via LLM, and dynamic prompt orchestration through MCP.

---

## 🔍 Tech Overview

- **Backend**: FastAPI (Python)  
- **Auth**: JWT for secure login/signup flows  
- **PDF → Markdown**: Extract content using libraries like PyMuPDF or PDFMiner  
- **LLM Integration**: Use *Mistral* for content summarization and markdown conversion  
- **Script Generation**: Custom logic to create engaging, conversational narration  
- **Prompts Management**: Prompts are stored and fetched remotely using the **Model Context Protocol (MCP)**, enabling version control and easy updates 

---

## ⚙️ Why MCP?

The *Model Context Protocol (MCP)* is an **open standard** introduced by Anthropic in November 2024. It allows LLM-powered apps to:
1. Discover available tools or prompts  
2. Fetch structured prompt templates via JSON‑RPC  
3. Maintain modular and updateable prompt logic separate from code  
[oai_citation: en.wikipedia.org](https://en.wikipedia.org/wiki/Model_Context_Protocol?utm_source=chatgpt.com)
[oai_citation: medium.com](https://medium.com/ai-cloud-lab/model-context-protocol-mcp-with-ollama-a-full-deep-dive-working-code-part-1-81a3bb6d16b3?utm_source=chatgpt.com) 
[oai_citation: blog.miloslavhomer.cz](https://blog.miloslavhomer.cz/p/tools-for-mistral-model-context-protocol?utm_source=chatgpt.com)

MCP is widely adopted by OpenAI, Google DeepMind, Microsoft, and many others as the “USB‑C for AI apps”  

---

## 🏗️ Architecture

```
User → FastAPI Endpoints → PDF Fetcher → Markdown Extractor →
Mistral LLM → Script Generator → Output 🎙️
↑
Prompts from MCP Server
```

---

## ✅ Feature List

- **JWT-Based Authentication**  
- **Paper Ingestion**: Submit ArXiv URLs or PDFs  
- **PDF → Markdown Extraction**  (Mistral OCR)
- **Mistral-Powered LLM** summarizing markdown into scripts  
- **Prompt Orchestration** with MCP server – remote fetch and version control  
- **Custom Narration Styles** – default presets + user-defined options  

---

## 🧑‍💻 Setup & Run

```bash
git clone https://github.com/…/PodcastAI.git
cd PodcastAI

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Backend

### Authentication flow

```bash
POST /auth/login
{
  "username": "your_user",
  "password": "secure_pass"
}
# → { "access_token": "jwt-token" }

GET /papers?url=https://arxiv.org/abs/…
Authorization: Bearer <jwt-token>
```
## 🧠 LLM + MCP Prompting
- MCP Client in your backend auto-discovers prompt templates.
- Makes JSON-RPC call to MCP server to get best practice and latest prompts.
- Sends paper’s markdown + prompt to Mistral to generate natural-language script.
- MCP centralizes prompt updates—improve narrator style without backend changes

## 📦 Sample Request & Response
```bash
POST /papers/request
Content-Type: application/json
Authorization: Bearer <token>

{
  "arxiv_url": "https://arxiv.org/abs/1706.03762",
  "style_id": "concise_explainer"
}
---
200 OK
{
  "script": "In this episode, we explore the Transformer architecture introduced in 2017..."
}
```

### 📌 Roadmap
- 🗣️ TTS Integration (e.g., ElevenLabs, Bark)
- 🔁 Job orchestration: background tasks with Celery or RQ
- 🧑‍🎓 Frontend/UI with live progress (FastAPI + WebSockets/Streamlit)
- 🎧 Podcast Publishing: export to RSS, audio stores