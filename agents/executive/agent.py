import logging
from typing import Dict, Any, List, Union, Optional
from agents.base import BaseAgent
from core.intelligence.recruiter_requirements import RecruiterRequirements
from core.intelligence.intent_parser import RecruiterIntentParser
from omium.tracing import trace

class ExecutiveAgent(BaseAgent):
    """
    Phase 5 & 7: Chief Recruitment Architect & Orchestrator.
    Dynamically plans and executes the hiring workflow.
    """
    
    def __init__(self, job_id: Optional[str] = None, db: Optional[Any] = None):
        super().__init__(name="Executive", role="Chief Recruitment Architect", job_id=job_id, db=db)
        self.intent_parser = RecruiterIntentParser()

    def plan_and_execute(self, query: str):
        """
        The Master Orchestration Loop.
        1. Planning (Intent Parsing)
        2. Extraction (BrowserAgent)
        3. Research & Technical Analysis (Fan-out)
        4. Ranking & Selection
        5. Reporting
        """
        trace("Workflow Planning Started")
        self.log(f"Planning workflow for query: {query}", step="planning")
        
        # 1. Parse Requirements
        requirements = self.intent_parser.parse(query)
        self.log(f"Autonomous strategy generated for {requirements.role}", step="planning")
        
        # 2. Assign Browser Agent for Extraction
        from agents.browser.agent import BrowserAgent
        browser_agent = BrowserAgent(job_id=self.job_id, db=self.db)
        candidates = browser_agent.run(requirements)
        
        if not candidates:
            self.log("No candidates found in extraction phase.", level=logging.ERROR, step="extraction")
            return []

        # 3. Dynamic Analysis & Scoring (Autonomous Branching)
        from agents.research.agent import ResearchAgent
        from agents.github.agent import GitHubAgent
        
        researcher = ResearchAgent(job_id=self.job_id, db=self.db)
        github_expert = GitHubAgent(job_id=self.job_id, db=self.db)
        
        final_candidates = []
        for candidate in candidates:
            self.log(f"Analyzing candidate: {candidate['name']}", step="scoring")
            
            # Semantic Research (LinkedIn content)
            candidate = researcher.run(candidate, requirements)
            
            # Conditional Branching: Only run GitHub agent if a footprint is suspected or found
            if candidate.get('github_url') or any(kw in candidate.get('headline', '').lower() for kw in ['git', 'developer', 'engineer', 'code']):
                candidate = github_expert.run(candidate, requirements)
            else:
                self.log(f"Skipping GitHub analysis for {candidate['name']} (No engineering footprint)", step="scoring")
                candidate['github_score'] = 10 # Default penalty
            
            final_candidates.append(candidate)

        # 4. Final Ranking
        ranked = self.rank_candidates(final_candidates, requirements)
        
        self.log(f"Workflow completed. Selected TOP {len(ranked)} candidates.", step="reporting")
        return ranked

    def rank_candidates(self, candidates: List[Dict[str, Any]], requirements: RecruiterRequirements) -> List[Dict[str, Any]]:
        """Enterprise Weighted Scoring Engine."""
        self.log("Executing final intelligence ranking...", step="ranking")
        
        for candidate in candidates:
            # Combine scores
            res_score = candidate.get('research_score', 0)
            git_score = candidate.get('github_score', 0)
            
            w_li = requirements.linkedin_weight
            w_gh = requirements.github_weight
            
            base_score = (res_score * w_li) + (git_score * w_gh)
            
            # Integrity adjustment
            readiness = candidate.get('readiness_score', 80) / 100
            final_score = base_score * readiness
            
            candidate['final_score'] = round(final_score, 2)
            
            # Generate reasoning explanation
            candidate['explanation'] = self._generate_explanation(candidate)

        candidates.sort(key=lambda x: x['final_score'], reverse=True)
        return candidates[:requirements.max_candidates]

    def _generate_explanation(self, candidate: Dict[str, Any]) -> str:
        score = candidate.get('final_score', 0)
        if score > 80:
            return f"Excellent match. Strong expertise in {candidate.get('headline')} with high engineering depth."
        elif score > 60:
            return f"Solid candidate. Good alignment with core skills, but moderate GitHub footprint."
        else:
            return "Potential match. Requires manual verification of technical depth."

    def run(self, query: str):
        return self.plan_and_execute(query)
