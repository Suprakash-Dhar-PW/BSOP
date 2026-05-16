import sys
import logging
import asyncio
from workflows.hiring import run_hiring_workflow

def main():
    """
    Entrypoint for the Business System Operations Platform (BSOP).
    """
    # Accept objective from command line args or use default
    objective = "Find frontend developers in Bengaluru"
    if len(sys.argv) > 1:
        objective = " ".join(sys.argv[1:])
        
    try:
        asyncio.run(run_hiring_workflow(objective))
    except Exception as e:
        logging.error(f"Workflow execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
