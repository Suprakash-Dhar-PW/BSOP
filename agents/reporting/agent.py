from typing import Dict, Any, List
from agents.base import BaseAgent

class ReportingAgent(BaseAgent):
    """
    Business Intelligence Reporting Engine.
    Compiles autonomous intelligence signals into enterprise-grade hiring reports.
    """
    
    def __init__(self):
        super().__init__(name="Reporting", role="Intelligence Reporter")
        
    def run(self, objective: str, candidates: List[Dict[str, Any]]) -> str:
        """
        Generates a high-fidelity intelligence report for the recruiter.
        Compiles all multi-agent signals into a cohesive decision-support document.
        """
        self.log("Generating enterprise-grade intelligence report...")
        
        # Helper to extract value from ConfidenceValue
        def get_val(obj):
            if hasattr(obj, 'value'): return obj.value
            if isinstance(obj, dict) and 'value' in obj: return obj['value']
            return obj or "N/A"

        def get_conf_stars(obj):
            conf = 0.0
            if hasattr(obj, 'confidence'): conf = obj.confidence
            elif isinstance(obj, dict) and 'confidence' in obj: conf = obj['confidence']
            
            if conf >= 0.9: return "⭐⭐⭐"
            if conf >= 0.6: return "⭐⭐"
            if conf >= 0.3: return "⭐"
            return "∅"

        report = []
        report.append("="*80)
        report.append(" " * 20 + "BSOP AUTONOMOUS HIRING INTELLIGENCE REPORT")
        report.append("="*80)
        report.append(f"RECRUITMENT OBJECTIVE: {objective.upper()}")
        report.append(f"TOTAL INTELLIGENCE ENTITIES RANKED: {len(candidates)}")
        report.append("="*80 + "\n")
        
        for i, c in enumerate(candidates, 1):
            name = c.get('name', 'Unknown')
            final_score = c.get('final_intelligence_score', 0)
            data_conf = c.get('extraction_confidence', 0)
            
            report.append(f"RANK #{i} | {name.upper()}")
            report.append(f"INTELLIGENCE SCORE: {final_score}/100 | DATA INTEGRITY: {data_conf}%")
            report.append("-" * 80)
            
            # Core Identity Signals
            report.append(f"  [IDENTITY]")
            report.append(f"    - Role Headline:  {get_val(c.get('headline'))} {get_conf_stars(c.get('headline'))}")
            report.append(f"    - Location:       {get_val(c.get('location'))} {get_conf_stars(c.get('location'))}")
            report.append(f"    - Specialization: {c.get('specialization', 'Generalist')}")
            report.append(f"    - Seniority:      {c.get('seniority', 'Mid-Level')} ({c.get('inferred_experience', 0)} yrs)")
            
            # Intelligence Signals
            report.append(f"  [INTELLIGENCE]")
            report.append(f"    - Research Score:  {c.get('research_score', 0)}% (LinkedIn Intelligence)")
            report.append(f"    - Technical Score: {c.get('github_score', 0)}% (Engineering Footprint)")
            
            # Technical Deep Dive
            report.append(f"  [TECHNICAL DEPTH]")
            report.append(f"    - GitHub:         {get_val(c.get('github')) or 'No technical signal linked'} {get_conf_stars(c.get('github'))}")
            
            req_matches = c.get('matched_required_skills', [])
            if req_matches:
                report.append(f"    - Validated Skills: {', '.join(req_matches)}")
            
            # Semantic Summaries
            report.append(f"  [EXECUTIVE SUMMARY]")
            report.append(f"    - Candidate: {c.get('intelligence_summary', 'N/A')}")
            report.append(f"    - Engineering: {c.get('technical_summary', 'N/A')}")
            
            report.append(f"  [LINKS]")
            report.append(f"    - LinkedIn: {c.get('profile_url')}")
            
            report.append("\n" + "."*80 + "\n")
            
        report.append("="*80)
        report.append(" " * 30 + "END OF INTELLIGENCE REPORT")
        report.append("="*80)
        
        return "\n".join(report)
