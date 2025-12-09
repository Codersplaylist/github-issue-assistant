"""
FastAPI backend for GitHub Issue Assistant.
Provides API endpoint for analyzing GitHub issues using AI.
"""
import time
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import uvicorn

from config import Config
from github_client import GitHubClient
from llm_analyzer import LLMAnalyzer


# Initialize FastAPI app
app = FastAPI(
    title="GitHub Issue Assistant API",
    description="AI-powered GitHub issue analysis and prioritization",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
github_client = GitHubClient()
llm_analyzer = LLMAnalyzer()

# Simple in-memory cache
cache: Dict[str, tuple] = {}  # {cache_key: (data, timestamp)}


class AnalyzeRequest(BaseModel):
    """Request model for issue analysis."""
    repo_url: str = Field(..., description="GitHub repository URL")
    issue_number: int = Field(..., gt=0, description="Issue number (must be positive)")
    
    @validator('repo_url')
    def validate_repo_url(cls, v):
        """Validate repository URL format."""
        if "github.com" not in v:
            raise ValueError("Must be a valid GitHub repository URL")
        return v.strip()


class AnalysisResponse(BaseModel):
    """Response model for issue analysis."""
    summary: str
    type: str
    priority_score: str
    suggested_labels: list[str]
    potential_impact: str
    metadata: Dict = Field(default_factory=dict)


def get_cache_key(repo_url: str, issue_number: int) -> str:
    """Generate cache key for an issue."""
    return f"{repo_url}::{issue_number}"


def get_from_cache(cache_key: str) -> Optional[Dict]:
    """Get data from cache if still valid."""
    if not Config.CACHE_ENABLED:
        return None
    
    if cache_key in cache:
        data, timestamp = cache[cache_key]
        # Check if cache is still valid
        if time.time() - timestamp < Config.CACHE_TTL:
            return data
        else:
            # Remove expired cache
            del cache[cache_key]
    
    return None


def set_cache(cache_key: str, data: Dict):
    """Store data in cache."""
    if Config.CACHE_ENABLED:
        cache[cache_key] = (data, time.time())


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "GitHub Issue Assistant API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze": "/api/analyze",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_issue(request: AnalyzeRequest):
    """
    Analyze a GitHub issue using AI.
    
    This endpoint fetches issue data from GitHub and uses an LLM to provide
    structured analysis including summary, type classification, priority scoring,
    suggested labels, and potential impact assessment.
    
    Args:
        request: AnalyzeRequest containing repo_url and issue_number
    
    Returns:
        AnalysisResponse with structured issue analysis
    
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Check cache first
        cache_key = get_cache_key(request.repo_url, request.issue_number)
        cached_data = get_from_cache(cache_key)
        
        if cached_data:
            return AnalysisResponse(**cached_data)
        
        # Fetch issue data from GitHub
        issue_data = github_client.get_issue_data(
            repo_url=request.repo_url,
            issue_number=request.issue_number
        )
        
        # Analyze with LLM
        analysis = llm_analyzer.analyze_issue(issue_data)
        
        # Add metadata
        response_data = {
            **analysis,
            "metadata": {
                "issue_url": issue_data.get("html_url", ""),
                "issue_state": issue_data.get("state", ""),
                "comments_count": issue_data.get("comments_count", 0),
                "created_at": issue_data.get("created_at", ""),
                "cached": False
            }
        }
        
        # Cache the result
        set_cache(cache_key, response_data)
        
        return AnalysisResponse(**response_data)
        
    except ValueError as e:
        # Client errors (invalid input, not found, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Server errors
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.delete("/api/cache")
async def clear_cache():
    """Clear the analysis cache."""
    cache.clear()
    return {"message": "Cache cleared successfully"}


if __name__ == "__main__":
    print("🚀 Starting GitHub Issue Assistant API...")
    print(f"📍 Server running at http://{Config.HOST}:{Config.PORT}")
    print(f"📚 API documentation at http://{Config.HOST}:{Config.PORT}/docs")
    
    uvicorn.run(
        "app:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )
