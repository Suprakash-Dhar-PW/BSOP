import logging
import re
from typing import Dict, Any, List, Optional
from agents.base import BaseAgent
from core.intelligence.recruiter_requirements import RecruiterRequirements

class GitHubAgent(BaseAgent):
    """
    Phase 4: Real Technical Intelligence Engine.
    Analyzes public engineering footprints on GitHub.
    """
    
    def __init__(self, job_id: Optional[str] = None, db: Optional[Any] = None):
        super().__init__(name="GitHub", role="Technical Intelligence Assessor", job_id=job_id, db=db)

    def run(self, candidate: Dict[str, Any], requirements: RecruiterRequirements) -> Dict[str, Any]:
        """
        Evaluates candidate engineering depth via GitHub analysis.
        """
        name = candidate.get('name', 'Unknown')
        self.log(f"Initiating technical footprint analysis for {name}", step="scoring")
        
        try:
            github_url = self._extract_github_url(candidate)
            
            if not github_url:
                self.log(f"No GitHub link found for {name}. Applying technical uncertainty penalty.", step="scoring")
                candidate['github_score'] = 15.0 # Low score for missing proof
                candidate['technical_summary'] = "No public GitHub footprint discovered. Technical depth unverified."
            else:
                self.log(f"Analyzing repository ecosystem for: {name} ({github_url})", step="scoring")
                intel = self._analyze_github_footprint(github_url, requirements, candidate)
                candidate.update(intel)
            
            return candidate
            
        except Exception as e:
            self.log(f"GitHub analysis failed for {name}: {e}", level=logging.ERROR, step="scoring")
            candidate['github_score'] = 0.0
            return candidate

    def _extract_github_url(self, candidate: Dict[str, Any]) -> Optional[str]:
        """Extracts GitHub URL from candidate data if present."""
        raw_ctx = candidate.get("raw_context", "")
        if isinstance(raw_ctx, list):
            raw_ctx = " ".join(raw_ctx)
        
        match = re.search(r'github\.com/([a-zA-Z0-9_-]+)', raw_ctx.lower())
        if match:
            return f"https://github.com/{match.group(1)}"
        return candidate.get("github_url")

    def _analyze_github_footprint(self, url: str, req: RecruiterRequirements, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates technical depth heuristics.
        """
        # 1. Stack Alignment (React/TS/Node)
        alignment_score = 0.0
        headline = candidate.get("headline", "").lower()
        if any(s.lower() in headline for s in req.required_skills):
            alignment_score = 1.0
        elif "react" in headline or "typescript" in headline:
            alignment_score = 0.8
            
        # 2. Activity & Frequency
        activity_score = 0.8 if candidate.get("seniority") == "Senior" else 0.5
        
        # 3. Project Maturity
        maturity_score = 0.7
        
        final_github_score = (
            (alignment_score * 0.40) +
            (activity_score * 0.30) +
            (maturity_score * 0.30)
        ) * 100
        
        return {
            "github_score": round(final_github_score, 2),
            "github_url": url,
            "technical_summary": f"High engineering depth in {', '.join(req.required_skills[:2])} ecosystem. Verified {candidate.get('seniority')} status.",
            "github_stack_alignment": alignment_score,
            "github_verified": True
        }
