from typing import Dict, Any, List
import time
from agents.base import BaseAgent

class ResearchAgent(BaseAgent):
    """
    Analyzes extracted data, compares skills, and ranks candidates based on requirements.
    """
    
    def __init__(self):
        super().__init__(name="Research", role="Data Analyst & Evaluator")
        
    def run(self, candidates: List[Dict[str, Any]], requirements: List[str]) -> List[Dict[str, Any]]:
        """Analyzes and ranks candidates against given requirements."""
        self.log(f"Analyzing {len(candidates)} candidates against requirements: {requirements}")
        time.sleep(1)
        
        ranked_candidates = []
        for candidate in candidates:
            self.log(f"Evaluating candidate: {candidate['name']}")
            
            # Simple simulation of skill matching
            matched_skills = [skill for skill in candidate['skills'] if any(req.lower() in skill.lower() for req in requirements)]
            match_score = len(matched_skills) / len(requirements) if requirements else 0
            
            # Experience multiplier (caps at 5 years for max score of 1.0)
            exp_score = min(candidate['experience_years'] / 5.0, 1.0) 
            
            final_score = (match_score * 0.7) + (exp_score * 0.3)
            
            candidate_analysis = candidate.copy()
            candidate_analysis['research_score'] = round(final_score * 100, 2)
            candidate_analysis['matched_skills'] = matched_skills
            ranked_candidates.append(candidate_analysis)
            
        # Sort by research score descending
        ranked_candidates.sort(key=lambda x: x['research_score'], reverse=True)
        self.log("Candidate evaluation and ranking complete.")
        
        return ranked_candidates
