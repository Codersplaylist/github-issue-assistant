"""
LLM-powered issue analyzer using Google Gemini.
Includes robust prompt engineering with few-shot examples.
"""
import json
import google.generativeai as genai
from typing import Dict, Optional
from config import Config


class LLMAnalyzer:
    """Analyzes GitHub issues using LLM with structured output."""
    
    def __init__(self):
        """Initialize the LLM analyzer with Gemini API."""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.LLM_MODEL)
        
    def create_prompt(self, issue_data: Dict) -> str:
        """
        Create a well-engineered prompt with few-shot examples.
        
        Args:
            issue_data: Dictionary containing issue information
        
        Returns:
            Formatted prompt string
        """
        # Truncate very long bodies to avoid token limits
        body = issue_data.get("body", "")
        if len(body) > 4000:
            body = body[:4000] + "\n... (truncated for length)"
        
        # Format comments
        comments_text = ""
        if issue_data.get("comments"):
            comments_list = issue_data["comments"][:10]  # Limit to first 10 comments
            for i, comment in enumerate(comments_list, 1):
                comment_body = comment.get("body", "")
                if len(comment_body) > 500:
                    comment_body = comment_body[:500] + "..."
                comments_text += f"\nComment {i} by {comment.get('author', 'unknown')}:\n{comment_body}\n"
        else:
            comments_text = "No comments yet."
        
        prompt = f"""You are an expert GitHub issue analyst. Analyze the following GitHub issue and provide a structured JSON response.

**IMPORTANT**: You must respond with ONLY valid JSON in the exact format specified below. Do not include any markdown, explanations, or text outside the JSON object.

Required JSON Format:
{{
  "summary": "A comprehensive, multi-sentence paragraph (approx 50-70 words) fully explaining the issue context, the problem, and the proposed solution.",
  "type": "One of: bug, feature_request, documentation, question, or other",
  "priority_score": "A number from 1-5 where 1=low, 2=minor, 3=moderate, 4=high, 5=critical. Include a full sentence justification.",
  "suggested_labels": ["2-3 relevant labels"],
  "potential_impact": "A detailed paragraph explaining the specific consequences for users, developers, and the business if this is not addressed."
}}

**Few-Shot Examples:**

Example 1 - Bug Report:
Issue Title: "Application crashes when clicking submit button"
Issue Body: "When I click the submit button on the login form, the app crashes immediately. This happens consistently on iOS 17."
Analysis:
{{
  "summary": "Login form submit button causes consistent app crashes on iOS 17",
  "type": "bug",
  "priority_score": "5 - Critical: Blocks core functionality (login) for all iOS 17 users",
  "suggested_labels": ["bug", "crash", "ios", "login"],
  "potential_impact": "Users cannot log in on iOS 17, completely blocking app access for this user segment"
}}

Example 2 - Feature Request:
Issue Title: "Add dark mode support"
Issue Body: "It would be great to have a dark mode option for better viewing at night."
Analysis:
{{
  "summary": "Request for dark mode theme option for improved nighttime viewing experience",
  "type": "feature_request",
  "priority_score": "2 - Low: Nice-to-have enhancement, not blocking any functionality",
  "suggested_labels": ["enhancement", "ui", "dark-mode"],
  "potential_impact": "Would improve user experience for users who prefer dark interfaces, but no current functionality is broken"
}}

Example 3 - Question:
Issue Title: "How to configure SSL certificates?"
Issue Body: "I'm trying to set up SSL but can't find documentation on where to place the certificates."
Analysis:
{{
  "summary": "User needs guidance on SSL certificate configuration and file placement",
  "type": "question",
  "priority_score": "3 - Moderate: Indicates documentation gap affecting user onboarding",
  "suggested_labels": ["question", "documentation", "ssl"],
  "potential_impact": "May indicate unclear documentation that could confuse other users during setup"
}}

---

Now analyze this issue:

**Issue Title:** {issue_data.get('title', 'No title')}

**Issue Body:**
{body if body else 'No description provided'}

**Comments:**
{comments_text}

**Existing Labels:** {', '.join(issue_data.get('labels', [])) if issue_data.get('labels') else 'None'}

Provide your analysis as valid JSON only:"""
        
        return prompt
    
    def parse_response(self, response_text: str) -> Dict:
        """
        Parse LLM response and extract JSON.
        
        Args:
            response_text: Raw response from LLM
        
        Returns:
            Parsed JSON dictionary
        
        Raises:
            ValueError: If response is not valid JSON
        """
        # Try to find JSON in the response
        response_text = response_text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            # Extract content between ```json and ```
            lines = response_text.split('\n')
            start_idx = 0
            end_idx = len(lines)
            
            for i, line in enumerate(lines):
                if line.strip().startswith("```"):
                    if start_idx == 0:
                        start_idx = i + 1
                    else:
                        end_idx = i
                        break
            
            response_text = '\n'.join(lines[start_idx:end_idx])
        
        try:
            data = json.loads(response_text)
            
            # Validate required fields
            required_fields = ["summary", "type", "priority_score", "suggested_labels", "potential_impact"]
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate type
            valid_types = ["bug", "feature_request", "documentation", "question", "other"]
            if data["type"] not in valid_types:
                data["type"] = "other"
            
            # Ensure suggested_labels is a list
            if not isinstance(data["suggested_labels"], list):
                data["suggested_labels"] = [str(data["suggested_labels"])]
            
            return data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {e}\nResponse: {response_text[:200]}")
    
    def analyze_issue(self, issue_data: Dict) -> Dict:
        """
        Analyze a GitHub issue using LLM.
        
        Args:
            issue_data: Dictionary containing issue information
        
        Returns:
            Structured analysis as dictionary
        
        Raises:
            ValueError: If analysis fails
        """
        try:
            # Create prompt
            prompt = self.create_prompt(issue_data)
            
            # Generate response with retry logic
            max_retries = 2
            last_error = None
            
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=Config.LLM_TEMPERATURE,
                            candidate_count=1,
                        )
                    )
                    
                    # Extract text from response
                    response_text = response.text
                    
                    # Parse and validate response
                    analysis = self.parse_response(response_text)
                    
                    return analysis
                    
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        continue
            
            # If all retries failed
            raise ValueError(f"LLM analysis failed after {max_retries} attempts: {last_error}")
            
        except Exception as e:
            # Provide fallback response in case of complete failure
            return {
                "summary": f"Analysis unavailable: {str(e)}",
                "type": "other",
                "priority_score": "3 - Unable to determine automatically",
                "suggested_labels": ["needs-triage"],
                "potential_impact": "Unable to analyze due to LLM error"
            }
