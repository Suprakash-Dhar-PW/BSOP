import os
import logging
import asyncio
from celery import Celery
from sqlalchemy.orm import Session
from .db.session import SessionLocal
from .models import crud, database
from agents.executive.agent import ExecutiveAgent

# Configure Celery
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("bsop_worker", broker=REDIS_URL, backend=REDIS_URL)

logger = logging.getLogger(__name__)

@celery_app.task(name="run_hiring_workflow")
def run_hiring_workflow_task(job_id: str, query: str):
    """
    Main Celery task to execute the autonomous hiring pipeline.
    """
    db = SessionLocal()
    try:
        # 1. Update status to running
        crud.update_search_status(db, job_id, "running")
        crud.log_workflow_event(db, job_id, "executive", "running", "Starting autonomous orchestration...")

        # 2. Initialize Executive Agent
        orchestrator = ExecutiveAgent(job_id=job_id, db=db)
        
        # 3. Run Pipeline asynchronously
        ranked_candidates = asyncio.run(orchestrator.run(query))
        
        # 4. Persist Final Results
        for rank, candidate in enumerate(ranked_candidates):
            # Save candidate and link to search
            crud.save_candidate_results(db, job_id, candidate, rank + 1)
            
        # 5. Mark as complete
        crud.update_search_status(db, job_id, "completed")
        crud.log_workflow_event(db, job_id, "executive", "completed", "Hiring intelligence generated successfully.")
        
    except Exception as e:
        logger.error(f"Autonomous workflow failed for job {job_id}: {str(e)}")
        crud.update_search_status(db, job_id, "failed")
        crud.log_workflow_event(db, job_id, "executive", "failed", f"Critical failure: {str(e)}")
    finally:
        db.close()
