import logging
from agents.executive.agent import ExecutiveAgent
from agents.browser.agent import BrowserAgent
from agents.research.agent import ResearchAgent
from agents.github.agent import GitHubAgent
from agents.reporting.agent import ReportingAgent
from omium.tracing import trace

logger = logging.getLogger("[Workflow Orchestrator]")

def run_hiring_workflow(objective: str):
    """
    Executes the end-to-end autonomous hiring workflow.
    """
    logger.info("Initializing BSOP Hiring Workflow...")
    trace("Workflow start")
    
    # 1. Instantiate Agents
    executive = ExecutiveAgent()
    browser = BrowserAgent()
    research = ResearchAgent()
    github = GitHubAgent()
    reporting = ReportingAgent()
    
    print("\n" + "="*60)
    print(">>> STARTING BSOP AUTONOMOUS WORKFLOW <<<")
    print("="*60 + "\n")
    
    # 2. Executive Planning
    trace("Executive planning")
    plan = executive.run(objective)
    
    # 3. Browser Agent: Search & Extract
    # The executive plan dictates what we do, but for this Phase 1, 
    # we explicitly orchestrate the handoffs based on the objective.
    trace("Browser agent execution")
    search_query = "Frontend Developer Bengaluru"
    candidates_data = browser.run(search_query)
    
    # 4. Research Agent: Analyze & Rank
    # Provide requirements based on objective
    trace("Research agent execution")
    job_requirements = ["React", "TypeScript", "Frontend", "JavaScript"]
    analyzed_candidates = research.run(candidates_data, job_requirements)
    
    # 5. GitHub Agent: Evaluate Code Quality
    trace("GitHub evaluation")
    final_candidates = github.run(analyzed_candidates)
    
    # 6. Reporting Agent: Generate Summary
    trace("Report generation")
    final_report = reporting.run(objective, final_candidates)
    
    print("\n\n")
    print(final_report)
    print("\n" + "="*60)
    print(">>> BSOP AUTONOMOUS WORKFLOW COMPLETED <<<")
    print("="*60 + "\n")
    trace("Workflow completion")

if __name__ == "__main__":
    run_hiring_workflow("Find frontend developers in Bengaluru")
