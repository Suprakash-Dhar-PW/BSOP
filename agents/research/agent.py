import re
import logging
from typing import Dict, Any, List, Optional
from agents.base import BaseAgent
from core.intelligence.recruiter_requirements import RecruiterRequirements

class ResearchAgent(BaseAgent):
    """
    Phase 3: Semantic Candidate Evaluator.
    Moves beyond simple keyword matching to deep semantic analysis of candidate experience.
    """
    
    def __init__(self, job_id: Optional[str] = None, db: Optional[Any] = None):
        super().__init__(name="Research", role="Hiring Intelligence Analyst", job_id=job_id, db=db)

    def run(self, candidate: Dict[str, Any], requirements: RecruiterRequirements) -> Dict[str, Any]:
        """
        Performs multi-dimensional semantic scoring on a single candidate entity.
        """
        name = candidate.get('name', 'Unknown')
        self.log(f"Evaluating semantic relevance for {name}", step="scoring")
        
        try:
            score_details = self._evaluate_candidate(candidate, requirements)
            
            analysis = {
                **candidate,
                **score_details,
                "research_analysis_v2": True
            }
            
            self.log(f"Semantic match for {name}: {analysis['research_score']}/100", step="scoring")
            return analysis
            
        except Exception as e:
            self.log(f"Semantic evaluation failed for {name}: {e}", level=logging.ERROR, step="scoring")
            return {**candidate, "research_score": 0, "error": str(e)}

    def _evaluate_candidate(self, candidate: Dict[str, Any], req: RecruiterRequirements) -> Dict[str, Any]:
        """
        Semantic Scoring Engine.
        """
        headline = candidate.get("headline", "").lower()
        about = candidate.get("about", "").lower()
        # Ensure raw_context is treated as string
        raw_ctx = candidate.get("raw_context", "")
        if isinstance(raw_ctx, list):
            raw_ctx = " ".join(raw_ctx)
        
        full_text = f"{headline} {about} {raw_ctx.lower()}"
        
        # 1. Role Relevance (30%)
        role_score = 0.0
        if req.role.lower() in headline:
            role_score = 1.0
        elif any(skill.lower() in headline for skill in req.required_skills):
            role_score = 0.7
        elif req.role.lower() in full_text:
            role_score = 0.5
            
        # 2. Engineering Depth & Stack Relevance (30%)
        stack_score = 0.0
        matched_skills = []
        if req.required_skills:
            for skill in req.required_skills:
                if skill.lower() in full_text:
                    matched_skills.append(skill)
            stack_score = len(matched_skills) / len(req.required_skills) if req.required_skills else 1.0
            
        # 3. Seniority & Experience Depth (20%)
        inferred_exp = 0
        exp_match = re.search(r'(\d+)\+?\s*years?', full_text)
        if exp_match:
            inferred_exp = int(exp_match.group(1))
        
        seniority = "Mid"
        if any(kw in full_text for kw in ["senior", "lead", "staff", "principle", "architect"]):
            seniority = "Senior"
            inferred_exp = max(inferred_exp, 5)
        elif any(kw in full_text for kw in ["junior", "entry", "associate"]):
            seniority = "Junior"
            inferred_exp = max(inferred_exp, 1)

        exp_score = min(inferred_exp / max(req.min_experience, 1), 1.2) if req.min_experience > 0 else 1.0
        
        # 4. Company Quality & Career Consistency (10%)
        company_score = 0.5
        if any(company.lower() in full_text for company in req.preferred_companies):
            company_score = 1.0
            
        # 5. Profile Maturity & Leadership (10%)
        leadership_score = 0.0
        if any(kw in full_text for kw in ["managed", "led", "mentored", "heading", "director", "vp"]):
            leadership_score = 1.0
            
        research_score = (
            (role_score * 0.30) +
            (stack_score * 0.30) +
            (exp_score * 0.20) +
            (company_score * 0.10) +
            (leadership_score * 0.10)
        ) * 100

        return {
            "research_score": round(research_score, 2),
            "role_relevance": round(role_score, 2),
            "stack_alignment": round(stack_score, 2),
            "seniority": seniority,
            "inferred_experience": inferred_exp,
            "matched_skills": matched_skills,
            "is_student": "student" in full_text or "university" in full_text,
            "is_intern": "intern" in full_text or "internship" in full_text,
            "leadership_indicators": leadership_score > 0
        }
