from typing import Dict, Any, List
from agents.base import BaseAgent

class ReportingAgent(BaseAgent):
    """
    Compiles data from multiple agents to generate final, structured business reports.
    """
    
    def __init__(self):
        super().__init__(name="Reporting", role="Business Intelligence Reporter")
        
    def run(self, workflow_objective: str, finalized_candidates: List[Dict[str, Any]]) -> str:
        """Generates a final formatted hiring summary report."""
        self.log("Generating final hiring summary report...")
        
        report = []
        report.append("="*60)
        report.append(f" BSOP EXECUTIVE SUMMARY: HIRING WORKFLOW")
        report.append("="*60)
        report.append(f"OBJECTIVE: {workflow_objective}")
        report.append(f"CANDIDATES PROCESSED: {len(finalized_candidates)}")
        report.append("-" * 60)
        
        for i, candidate in enumerate(finalized_candidates, 1):
            report.append(f"[{i}] {candidate['name']} - {candidate.get('headline', 'N/A')}")
            report.append(f"    Location:      {candidate['location']}")
            report.append(f"    Experience:    {candidate['experience_years']} years")
            report.append(f"    Top Skills:    {', '.join(candidate['skills'])}")
            report.append(f"    Research Score: {candidate.get('research_score', 'N/A')}/100")
            report.append(f"    GitHub Score:   {candidate.get('github_score', 'N/A')}/100")
            report.append(f"    FINAL SCORE:    {candidate.get('final_hiring_score', 'N/A')}/100")
            report.append(f"    Code Summary:   {candidate.get('code_quality_summary', 'N/A')}")
            report.append("-" * 60)
            
        report_text = "\n".join(report)
        self.log("Report generation complete.")
        
        return report_text
