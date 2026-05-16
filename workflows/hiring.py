import logging
import asyncio
from typing import Dict, Any, Union
from agents.executive.agent import ExecutiveAgent
from agents.browser.agent import BrowserAgent
from agents.research.agent import ResearchAgent
from agents.github.agent import GitHubAgent
from agents.reporting.agent import ReportingAgent
from config.schemas import RecruiterRequirements
from omium.tracing import trace

logger = logging.getLogger("[Workflow Orchestrator]")

async def run_hiring_workflow(input_data: Union[str, Dict[str, Any]]):
    """
    Executes the BSOP Autonomous Hiring Intelligence Workflow.
    Now fully recruiter-driven and dynamic.
    
    1. Intent Architecture: Translates recruiter requirements into agent strategies.
    2. Entity Discovery: Deep browser-based candidate extraction.
    3. Intelligence Analysis: Semantic profile and technical evaluation.
    4. Enterprise Ranking: Weighted scoring based on recruiter intent.
    """
    logger.info("Initializing BSOP Autonomous Hiring Intelligence Platform...")
    trace("Workflow Started")
    
    # 1. Initialize Autonomous Workforce
    executive = ExecutiveAgent()
    reporting = ReportingAgent()
    
    try:
        print("\n" + "="*80)
        print(">>> BSOP AUTONOMOUS HIRING INTELLIGENCE PLATFORM <<<")
        print("="*80 + "\n")
        
        # 2. Executive: Recruiter Intent Engine & Full Execution
        trace("Executive Requirements Engineering")
        
        # Parse objective for reporting and requirements
        if isinstance(input_data, str):
            # Parse it to a dict first to map RecruiterIntent to RecruiterRequirements
            intent = executive.intent_parser.parse(input_data)
            requirements = RecruiterRequirements(
                role=intent.role,
                location=intent.location or "Remote",
                required_skills=intent.skills,
                preferred_companies=intent.preferred_companies,
            )
        else:
            requirements = RecruiterRequirements(**input_data)

        # The executive agent orchestrates browser, research, and github internally
        # Executive Agent expects the raw string query if it's a string, or requirements.
        
        ranked_candidates = await executive.run(input_data)

        self_objective = requirements.role + " in " + requirements.location
        
        # 7. Reporting Agent: Enterprise Intelligence Summary
        trace("Report Generation")
        intelligence_report = reporting.run(self_objective, ranked_candidates)
        
        print(intelligence_report)
        print("\n" + "="*80)
        print(">>> BSOP WORKFLOW COMPLETED SUCCESSFULLY <<<")
        print("="*80 + "\n")
        trace("Workflow Completed")
        
    except Exception as e:
        logger.error(f"Workflow Critical Failure: {e}")
        import traceback
        logger.error(traceback.format_exc())
        trace("Workflow Failed")

if __name__ == "__main__":
    recruiter_intent = {
        "role": "Backend Engineer",
        "location": "Bengaluru",
        "required_skills": ["Node.js", "PostgreSQL", "Redis"],
        "preferred_skills": ["AWS", "Docker", "Kafka"],
        "minimum_experience": 4,
        "exclude_students": True,
        "exclude_interns": True,
        "preferred_companies": ["Google", "Amazon", "Razorpay"],
        "github_weight": 0.4,
        "linkedin_weight": 0.6,
        "max_candidates": 3
    }
    
    asyncio.run(run_hiring_workflow(recruiter_intent))
