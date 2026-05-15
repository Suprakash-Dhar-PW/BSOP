from typing import Dict, Any, List
import time
from agents.base import BaseAgent

class GitHubAgent(BaseAgent):
    """
    Evaluates candidate GitHub repositories for engineering quality.
    Will later integrate with GitHub MCP.
    """
    
    def __init__(self):
        super().__init__(name="GitHub", role="Code Quality Assessor")
        
    def run(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Simulates evaluation of GitHub repositories for each candidate."""
        self.log(f"Starting GitHub evaluation for {len(candidates)} candidates...")
        time.sleep(1)
        
        evaluated_candidates = []
        for candidate in candidates:
            github_url = candidate.get('github')
            if not github_url:
                self.log(f"Skipping {candidate['name']} - No GitHub URL provided.")
                candidate['github_score'] = 0
                candidate['code_quality_summary'] = "No repository data."
                candidate['final_hiring_score'] = round((candidate.get('research_score', 0) * 0.6), 2)
                evaluated_candidates.append(candidate)
                continue
                
            self.log(f"Analyzing repositories for {candidate['name']} at {github_url}...")
            
            # Simulate GitHub data extraction and scoring
            if "aarav" in github_url.lower():
                score = 92
                summary = "Excellent commit history. High-quality React components with solid test coverage."
            elif "priya" in github_url.lower():
                score = 85
                summary = "Good Vue.js projects. Consistent commits, but lacks automated tests."
            else:
                score = 75
                summary = "A few UI prototypes. Commits are sporadic, code formatting is inconsistent."
                
            candidate_eval = candidate.copy()
            candidate_eval['github_score'] = score
            candidate_eval['code_quality_summary'] = summary
            
            # Calculate a combined final score
            research_score = candidate_eval.get('research_score', 0)
            candidate_eval['final_hiring_score'] = round((research_score * 0.6) + (score * 0.4), 2)
            
            evaluated_candidates.append(candidate_eval)
            
        # Sort by final hiring score descending
        evaluated_candidates.sort(key=lambda x: x['final_hiring_score'], reverse=True)
        self.log("GitHub evaluations complete.")
        
        return evaluated_candidates
