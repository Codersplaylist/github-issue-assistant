# GitHub Issue Assistant

A full-stack application that leverages the Google Gemini LLM to analyze, prioritize, and summarize GitHub issues. This tool automates the triage process, helping maintainers save time by providing instant context and actionable labels.

## 🎯 Project Goal

The primary goal of this project was to build a vertically integrated AI application that solves a real-world problem: **Information Overload in Open Source**.

By piping raw GitHub issue data into a structured LLM prompt, this assistant transforms unstructured text into structured JSON data (priority scores, summaries, impact analysis) that can be easily consumed by developers.

## 🛠️ Technical Stack

*   **Backend**: Python 3.12+, FastAPI (for asynchronous request handling)
*   **AI Engine**: Google Gemini 1.5/2.0 Flash (via `google-generativeai` SDK)
*   **Frontend**: Vanilla JavaScript & CSS (No heavy frameworks, focused on performance)
*   **Networking**: `httpx` for async GitHub API calls
*   **State Management**: In-memory caching

## High level diagram
<img width="1009" height="407" alt="Screenshot 2025-12-19 at 02 24 11" src="https://github.com/user-attachments/assets/0d3434af-3f5a-4b68-8a73-f1d3e64b4ae4" />



## 🏗️ Architecture & Design Decisions

### 1. Asynchronous Backend (FastAPI)
I chose FastAPI over Flask/Django because LLM and GitHub API requests are I/O bound. FastAPI's `async/await` support allows the server to handle multiple analysis requests concurrently without blocking the main thread, which is critical for an API dependent on third-party services.

### 2. Prompt Engineering Strategy
The core intelligence lives in `backend/llm_analyzer.py`. I implemented a **Few-Shot Prompting** strategy:
*   Instead of asking the model generically to "analyze this," I provide it with concrete examples of input/output pairs for a more accurate priority score.
*   The prompt enforces a strict JSON schema output, ensuring the frontend never breaks due to malformed AI responses.
*   I specifically tune the `temperature` to `0.1` to ensure deterministic, factual results rather than creative hallucinations.

### 3. Smart Caching
To respect API rate limits and reduce latency, I implemented a custom caching layer (`backend/app.py`). It stores analysis results indexed by `repo_url + issue_number`. This means repeated requests for the same issue are instant (0ms latency), dramatically improving the user experience for popular issues.(TTL=1hr)

### 4. Zero-Dependency Frontend
For the UI, I avoided heavy bundles like React or Angular. By using modern Vanilla JS and CSS Variables:
*   The site loads instantly.
*   The code is cleaner and easier to audit.
*   It demonstrates core understanding of the DOM and CSS Grid/Flexbox without relying on abstractions.

## 🚀 Setup & Installation

### Prerequisites
*   Python 3.9+
*   A Google Gemini API Key

## Usage

1.  Paste a GitHub repository URL (e.g., `https://github.com/facebook/react`).
2.  Enter an issue number (e.g., `28858`).
3.  Click **Analyze**.
4.  The system will fetch the raw data, process it through the LLM pipeline, and render a complete report.
## Screenshot
<img width="1432" height="709" alt="Screenshot 2025-12-19 at 02 29 48" src="https://github.com/user-attachments/assets/8d6eec1b-3170-4557-a375-866005d016c2" />
<img width="1193" height="763" alt="Screenshot 2025-12-19 at 02 30 16" src="https://github.com/user-attachments/assets/d3bb8b7d-de86-4382-adfe-920454d91451" />

## Future Improvements

If I were to expand this project, I would focus on:
1.  **RAG (Retrieval Augmented Generation)**: Indexing the entire repository codebase so the AI can check if the issue relates to specific files.
2.  **Webhook Integration**: Automatically analyzing issues as soon as they are opened on GitHub via Webhooks.
3.  **Database Layer**: Moving from in-memory caching to Redis for persistence across server restarts.
