# 🚀 GitHub Issue Assistant

> AI-Powered GitHub Issue Analysis & Prioritization

An intelligent web application that leverages Large Language Models to automatically analyze GitHub issues, providing structured insights including summaries, type classification, priority scoring, label suggestions, and impact assessment.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=flat&logo=google)](https://ai.google.dev/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python)](https://www.python.org/)

## ✨ Features

- **🤖 AI-Powered Analysis**: Uses Google Gemini LLM with carefully crafted prompts and few-shot examples
- **📊 Structured Output**: Returns consistent JSON analysis with summary, type, priority, labels, and impact
- **⚡ Fast & Efficient**: Built-in caching mechanism to avoid redundant API calls
- **🎨 Premium UI**: Modern dark theme with glassmorphism, smooth animations, and responsive design
- **🛡️ Robust Error Handling**: Gracefully handles edge cases like missing comments, rate limits, and long issue bodies
- **📋 Copy to Clipboard**: One-click JSON export for easy integration
- **🔍 Example Issues**: Quick-fill buttons for testing with real GitHub issues

## 🏗️ Architecture

```
github-issue-assistant/
├── backend/                 # FastAPI backend
│   ├── app.py              # Main application & API endpoints
│   ├── config.py           # Configuration management
│   ├── github_client.py    # GitHub API integration
│   ├── llm_analyzer.py     # LLM integration with prompt engineering
│   └── requirements.txt    # Python dependencies
├── frontend/                # Modern web frontend
│   ├── index.html          # Main HTML structure
│   ├── style.css           # Premium dark theme styles
│   └── script.js           # Frontend logic & API communication
├── .env.example            # Environment template
├── .gitignore              # Git ignore patterns
└── README.md               # This file
```

## 🚀 Quick Start (< 5 Minutes)

### Prerequisites

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Google Gemini API Key** ([Get Free Key](https://aistudio.google.com/app/apikey))
- **Git** (optional, for cloning)

### Step 1: Clone or Download

```bash
git clone <your-repo-url>
cd github-issue-assistant
```

### Step 2: Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure API Key

Create a `.env` file in the **root directory** (not in backend/) with your Gemini API key:

```bash
# In the github-issue-assistant/ root directory
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

**Getting a Gemini API Key:**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and paste it in your `.env` file

### Step 4: Start the Backend

```bash
# From the backend/ directory (with venv activated)
python app.py
```

You should see:
```
🚀 Starting GitHub Issue Assistant API...
📍 Server running at http://0.0.0.0:8000
📚 API documentation at http://0.0.0.0:8000/docs
```

### Step 5: Start the Frontend

Open a **new terminal** window:

```bash
# Navigate to frontend directory
cd frontend

# Start a simple HTTP server
python -m http.server 3000
```

### Step 6: Use the Application

1. Open your browser and go to **http://localhost:3000**
2. Enter a GitHub repository URL (e.g., `https://github.com/facebook/react`)
3. Enter an issue number (e.g., `28858`)
4. Click **"Analyze Issue"** and watch the AI work! ✨

**Or try the example chips for instant testing!**

## 📖 Usage Examples

### Example 1: Analyzing a React Issue

```
Repository URL: https://github.com/facebook/react
Issue Number: 28858
```

### Example 2: Analyzing a VS Code Issue

```
Repository URL: https://github.com/microsoft/vscode
Issue Number: 200000
```

### Example 3: Using the API Directly

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/facebook/react",
    "issue_number": 28858
  }'
```

## 🎯 API Response Format

```json
{
  "summary": "One-sentence summary of the issue",
  "type": "bug | feature_request | documentation | question | other",
  "priority_score": "1-5 with justification",
  "suggested_labels": ["label1", "label2", "label3"],
  "potential_impact": "Brief impact description",
  "metadata": {
    "issue_url": "https://github.com/...",
    "issue_state": "open | closed",
    "comments_count": 5,
    "created_at": "2024-01-01T00:00:00Z",
    "cached": false
  }
}
```

## 🧠 How It Works

### 1. **GitHub Data Fetching**
- Parses repository URL to extract owner and repo name
- Fetches issue title, body, and comments via GitHub API
- Handles rate limits and authentication (optional GitHub token for higher limits)

### 2. **AI Analysis**
- Uses **Google Gemini 1.5 Flash** for fast, accurate analysis
- Employs **few-shot prompting** with real examples for consistent output
- Includes **retry logic** and **fallback responses** for reliability
- Truncates long issue bodies to stay within token limits

### 3. **Smart Caching**
- Caches analysis results in memory (1 hour TTL by default)
- Avoids redundant API calls for the same issue
- Reduces costs and improves response times

### 4. **Edge Cases Handled**
- ✅ Issues with no comments
- ✅ Very long issue bodies (>5000 chars)
- ✅ Invalid repository URLs
- ✅ Non-existent issue numbers
- ✅ GitHub API rate limiting
- ✅ LLM response parsing errors
- ✅ Network timeouts

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - GitHub token for higher rate limits (5000/hr vs 60/hr)
GITHUB_TOKEN=your_github_token_here

# Optional - Server configuration
HOST=0.0.0.0
PORT=8000

# Optional - LLM settings
LLM_MODEL=gemini-1.5-flash
LLM_TEMPERATURE=0.1

# Optional - Cache settings
CACHE_ENABLED=true
CACHE_TTL=3600
```

### Getting a GitHub Token (Optional but Recommended)

1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name like "Issue Assistant"
4. **No scopes needed** for public repositories
5. Copy the token and add to `.env`

## 🎨 Design Philosophy

This application showcases **modern web design principles**:

- **Dark Mode First**: Easy on the eyes, professional appearance
- **Glassmorphism**: Frosted glass effects with backdrop blur
- **Vibrant Gradients**: Eye-catching color schemes
- **Smooth Animations**: Micro-interactions enhance UX
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Accessibility**: Semantic HTML, proper contrast ratios

## 🧪 Testing

### Manual Testing Checklist

- [x] Valid issue analysis works correctly
- [x] Error handling for invalid URLs
- [x] Error handling for non-existent issues  
- [x] Loading states appear during analysis
- [x] Copy to clipboard functionality works
- [x] Example chips populate form correctly
- [x] Caching reduces subsequent request time
- [x] Responsive design on mobile devices

### API Documentation

Visit **http://localhost:8000/docs** when the backend is running to see interactive API documentation powered by Swagger UI.

## 🚨 Troubleshooting

### "GEMINI_API_KEY is required"

**Solution**: Make sure you've created a `.env` file in the **root directory** with your API key.

### "Connection refused" or CORS errors

**Solution**: 
1. Ensure the backend is running on port 8000
2. Ensure the frontend is accessing `http://localhost:8000` (check `script.js`)

### "GitHub API rate limit exceeded"

**Solution**: 
1. Add a `GITHUB_TOKEN` to your `.env` file (see Configuration section)
2. This increases your rate limit from 60 to 5000 requests/hour

### Frontend shows blank page

**Solution**: 
1. Check browser console for errors (F12 → Console)
2. Ensure you're accessing `http://localhost:3000` (not file://)

## 📦 Project Structure Explained

### Backend Components

- **`app.py`**: FastAPI application with `/api/analyze` endpoint, CORS, caching
- **`github_client.py`**: GitHub API wrapper with URL parsing and data fetching
- **`llm_analyzer.py`**: Gemini integration with prompt engineering
- **`config.py`**: Centralized configuration with validation

### Frontend Components

- **`index.html`**: Semantic HTML structure with form, results, notifications
- **`style.css`**: Modern CSS with custom properties, animations, glassmorphism
- **`script.js`**: Vanilla JavaScript for API calls, DOM manipulation, clipboard

## 🔮 Future Enhancements

- [ ] **Database persistence**: Store analysis history
- [ ] **Batch analysis**: Analyze multiple issues at once
- [ ] **Export options**: PDF, CSV export
- [ ] **GitHub OAuth**: Direct integration with user's repos
- [ ] **Advanced filters**: Filter by priority, type, labels
- [ ] **Real-time updates**: WebSocket for live analysis
- [ ] **Team collaboration**: Share analysis with team members

## 📄 License

MIT License - Feel free to use this project for learning and development!

## 🙏 Acknowledgments

- **FastAPI**: For the amazing Python web framework
- **Google Gemini**: For powerful LLM capabilities
- **GitHub API**: For comprehensive issue data access
- **Seedling Labs**: For the inspiring challenge

---

**Built with ❤️ for Seedling Labs**

Need help? Found a bug? [Open an issue](../../issues) or submit a pull request!
