"""
GitHub API client for fetching issue data.
Handles URL parsing, API requests, and error handling.
"""
import re
import requests
from typing import Dict, List, Optional, Tuple
from config import Config


class GitHubClient:
    """Client for interacting with the GitHub API."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self):
        """Initialize the GitHub client with optional authentication."""
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Issue-Assistant/1.0"
        })
        
        # Add authentication if token is provided (increases rate limits)
        if Config.GITHUB_TOKEN:
            self.session.headers["Authorization"] = f"token {Config.GITHUB_TOKEN}"
    
    def parse_repo_url(self, repo_url: str) -> Tuple[str, str]:
        """
        Parse a GitHub repository URL to extract owner and repo name.
        
        Args:
            repo_url: GitHub repository URL (e.g., https://github.com/owner/repo)
        
        Returns:
            Tuple of (owner, repo_name)
        
        Raises:
            ValueError: If URL format is invalid
        """
        # Support multiple URL formats
        patterns = [
            r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$",
            r"github\.com/([^/]+)/([^/]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, repo_url)
            if match:
                owner, repo = match.groups()
                # Clean repo name from any trailing slashes or .git
                repo = repo.rstrip('/').replace('.git', '')
                return owner, repo
        
        raise ValueError(
            f"Invalid GitHub repository URL: {repo_url}. "
            "Expected format: https://github.com/owner/repo"
        )
    
    def fetch_issue(self, owner: str, repo: str, issue_number: int) -> Dict:
        """
        Fetch issue data from GitHub API.
        
        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number
        
        Returns:
            Dictionary containing issue data
        
        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues/{issue_number}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError(
                    f"Issue #{issue_number} not found in {owner}/{repo}. "
                    "Please check the repository and issue number."
                )
            elif response.status_code == 403:
                raise ValueError(
                    "GitHub API rate limit exceeded. "
                    "Please add a GITHUB_TOKEN to your .env file for higher limits."
                )
            else:
                raise ValueError(f"GitHub API error: {e}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to connect to GitHub API: {e}")
    
    def fetch_comments(self, owner: str, repo: str, issue_number: int) -> List[Dict]:
        """
        Fetch comments for a specific issue.
        
        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number
        
        Returns:
            List of comment dictionaries
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues/{issue_number}/comments"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            # If comments fail, return empty list (non-critical)
            return []
    
    def get_issue_data(self, repo_url: str, issue_number: int) -> Dict:
        """
        Complete pipeline to fetch issue and its comments.
        
        Args:
            repo_url: GitHub repository URL
            issue_number: Issue number
        
        Returns:
            Dictionary with structured issue data
        """
        # Parse repository URL
        owner, repo = self.parse_repo_url(repo_url)
        
        # Fetch issue data
        issue = self.fetch_issue(owner, repo, issue_number)
        
        # Fetch comments
        comments = self.fetch_comments(owner, repo, issue_number)
        
        # Extract relevant data
        return {
            "title": issue.get("title", ""),
            "body": issue.get("body") or "",  # Handle None case
            "state": issue.get("state", ""),
            "labels": [label["name"] for label in issue.get("labels", [])],
            "comments_count": issue.get("comments", 0),
            "comments": [
                {
                    "author": comment.get("user", {}).get("login", "unknown"),
                    "body": comment.get("body", ""),
                    "created_at": comment.get("created_at", "")
                }
                for comment in comments
            ],
            "created_at": issue.get("created_at", ""),
            "html_url": issue.get("html_url", "")
        }
