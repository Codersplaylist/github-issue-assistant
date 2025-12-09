# GitHub Issue Assistant

This is a web application that helps analyze GitHub issues using AI. It uses the Google Gemini API to read an issue and tell you what type of issue it is, how important it is, and give a summary.

## Features

*   **AI Analysis**: Uses Google Gemini to read issues.
*   **Simple Interface**: Easy to use web interface.
*   **Fast**: Caches results so you don't have to wait if you analyze the same issue twice.

## Project Structure

*   `backend/`: Contains the Python FastAPI server.
*   `frontend/`: Contains the HTML/CSS/JS for the website.

## Setup Instructions

### Prerequisites

*   Python 3.9 or higher
*   Google Gemini API Key

### 1. Backend Setup

Go to the backend folder and install the requirements:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a file named `.env` in the main folder (not backend) and add your API key:

```
GEMINI_API_KEY=your_key_here
```

Start the server:

```bash
python app.py
```

### 2. Frontend Setup

Open a new terminal, go to the frontend folder, and start a simple server:

```bash
cd frontend
python -m http.server 3000
```

### 3. Usage

Open your browser and go to `http://localhost:3000`. Enter a GitHub repository URL and an issue number to analyze it.

## API Endpoints

*   `POST /api/analyze`: Analyzes an issue. requires `repo_url` and `issue_number`.

## License

MIT License.
