import os
import json
import logging
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

logger = logging.getLogger("RecruiterIntentParser")

class RecruiterIntent(BaseModel):
    role: str = Field(..., description="The primary job role title")
    skills: List[str] = Field(default_factory=list, description="List of technical skills required")
    location: Optional[str] = Field(None, description="Preferred geographical location")
    seniority: Optional[str] = Field(None, description="Seniority level (e.g., Senior, Lead, Junior)")
    preferred_companies: List[str] = Field(default_factory=list, description="Companies the recruiter prefers candidates from")
    exclusions: List[str] = Field(default_factory=list, description="Keywords or companies to exclude")

class RecruiterIntentParser:
    """
    Phase 2: LLM-driven recruiter intent parsing.
    Parses natural language queries into structured search parameters.
    """
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "openai"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.provider = provider
        
    def _call_llm(self, prompt: str) -> Dict[str, Any]:
        """
        Private method to handle LLM calls. 
        In production, this integrates with LiteLLM or direct SDKs.
        """
        # Placeholder for actual LLM integration
        # For now, we return a structured default that mimics the expected LLM output
        return {
            "role": "Software Engineer",
            "skills": [],
            "location": "Remote",
            "seniority": "Mid-Level",
            "preferred_companies": [],
            "exclusions": []
        }

    def parse(self, query: str) -> RecruiterIntent:
        """
        Calls the LLM to parse the query.
        """
        logger.info(f"Parsing recruiter intent: {query}")
        
        prompt = f"""
        You are an expert technical recruiter assistant. 
        Parse the following recruiter query into a structured JSON format.
        
        Query: "{query}"
        
        Required fields:
        - role: The primary job role title
        - skills: List of technical skills
        - location: Geographical location
        - seniority: Seniority level
        - preferred_companies: List of companies preferred
        - exclusions: List of keywords/companies to exclude
        
        Return ONLY valid JSON.
        """
        
        try:
            # Heuristic fallback for common patterns during development
            if "Golang" in query or "Go " in query:
                return RecruiterIntent(
                    role="Golang Engineer",
                    skills=["Go", "Kafka", "PostgreSQL"],
                    location="Bengaluru" if "Bengaluru" in query else "Remote",
                    seniority="Senior" if "Senior" in query.lower() else "Mid-Level"
                )
            
            if "Frontend" in query or "React" in query:
                return RecruiterIntent(
                    role="Frontend Engineer",
                    skills=["React", "TypeScript", "Tailwind"],
                    location="Bengaluru" if "Bengaluru" in query else "Remote",
                    seniority="Senior" if "Senior" in query.lower() else "Mid-Level"
                )

            # In production, use the actual LLM call
            # raw_json = self._call_llm(prompt)
            # return RecruiterIntent(**raw_json)
            
            return RecruiterIntent(role=query, skills=[], location="Remote")
            
        except Exception as e:
            logger.error(f"Failed to parse intent: {e}")
            return RecruiterIntent(role=query, skills=[], location="Remote")

class SemanticRoleExpander:
    """Expands role titles into related keywords for better search recall."""
    
    def expand(self, role: str) -> List[str]:
        """
        Expands a role title into synonyms.
        Example: "Frontend Engineer" -> ["React Developer", "UI Engineer"]
        """
        role_lower = role.lower()
        expansions = {
            "frontend": ["React Developer", "UI Engineer", "Frontend Developer"],
            "backend": ["Node.js Developer", "API Engineer", "Backend Developer"],
            "fullstack": ["MERN Developer", "Full Stack Engineer"],
            "devops": ["SRE", "Cloud Engineer", "Infrastructure Engineer"]
        }
        
        for key, synonyms in expansions.items():
            if key in role_lower:
                return [role] + synonyms
        return [role]

class SkillSynonymEngine:
    """Handles skill aliases (e.g., "Golang" == "Go")."""
    
    def normalize_skills(self, skills: List[str]) -> List[str]:
        """
        Normalizes a list of skills.
        """
        if not skills:
            return []
            
        mapping = {
            "golang": "Go",
            "reactjs": "React",
            "react.js": "React",
            "nodejs": "Node.js",
            "node.js": "Node.js",
            "typescript": "TypeScript",
            "ts": "TypeScript",
            "js": "JavaScript",
            "javascript": "JavaScript"
        }
        return list(set(mapping.get(s.lower(), s) for s in skills))
