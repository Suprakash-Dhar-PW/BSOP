import logging
from typing import Dict, Any, Union
from agents.executive.agent import ExecutiveAgent
from agents.browser.agent import BrowserAgent
from agents.research.agent import ResearchAgent
from agents.github.agent import GitHubAgent
from agents.reporting.agent import ReportingAgent
from config.schemas import RecruiterRequirements
from omium.tracing import trace

logger = logging.getLogger("[Workflow Orchestrator]")

def run_hiring_workflow(input_data: Union[str, Dict[str, Any]]):
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
    browser = BrowserAgent()
    research = ResearchAgent()
    github = GitHubAgent()
    reporting = ReportingAgent()
    
    try:
        print("\n" + "="*80)
        print(">>> BSOP AUTONOMOUS HIRING INTELLIGENCE PLATFORM <<<")
        print("="*80 + "\n")
        
        # 2. Executive: Recruiter Intent Engine
        # Architect requirements and dynamic search strategy
        trace("Executive Requirements Engineering")
        requirements: RecruiterRequirements = executive.run(input_data)
        
        self_objective = requirements.role + " in " + requirements.location
        
        # 3. Browser Agent: Entity-Centric Discovery
        # Searches and extracts candidate entities using dynamic search strategy
        trace("Browser Intelligence Discovery")
        candidate_entities = browser.run(requirements)
        
        if not candidate_entities:
            logger.error("No candidate entities discovered. Workflow terminated.")
            return

        # 4. Research Agent: Intelligent Semantic Analysis
        # Evaluates required/preferred skills, seniority, and specialization
        trace("Research Intelligence Analysis")
        analyzed_candidates = research.run(candidate_entities, requirements)
        
        if not analyzed_candidates:
            logger.warning("All candidates filtered out during research analysis.")
            return

        # 5. GitHub Agent: Technical Depth Evaluation
        # Analyzes engineering footprint based on recruiter stack requirements
        trace("Technical Depth Evaluation")
        technical_candidates = github.run(analyzed_candidates, requirements)
        
        # 6. Executive: Final Recruiter-Weighted Ranking
        # Implements the Enterprise Scoring System based on dynamic intent
        trace("Final Intelligence Ranking")
        ranked_candidates = executive.rank_candidates(technical_candidates, requirements)
        
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
    finally:
        browser.close()

if __name__ == "__main__":
    # Example 1: High-level recruitment objective (parsed by ExecutiveAgent)
    # run_hiring_workflow("Find top-tier Frontend Engineers in Bengaluru with React and TypeScript expertise")
    
    # Example 2: Structured Recruiter Requirements (Direct Intent)
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
    
    run_hiring_workflow(recruiter_intent)
