from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uuid
import logging
from sqlalchemy.orm import Session

from .db.session import SessionLocal, engine
from .models import database, crud
from .worker.tasks import run_hiring_workflow

# Create tables if they don't exist
database.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BSOP Autonomous Hiring Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/search", response_model=dict)
async def create_search(query: str, db: Session = Depends(get_db)):
    """
    Triggers a new autonomous hiring workflow.
    """
    job_id = str(uuid.uuid4())
    
    # 1. Persist Job
    crud.create_search_job(db, job_id, query)
    
    # 2. Queue Celery Task
    run_hiring_workflow.delay(job_id, query)
    
    return {
        "job_id": job_id,
        "status": "queued",
        "message": "Autonomous search started."
    }

@app.get("/search/{job_id}", response_model=dict)
async def get_search_status(job_id: str, db: Session = Depends(get_db)):
    """
    Returns real progress and status from DB.
    """
    search = db.query(database.Search).filter(database.Search.id == job_id).first()
    if not search:
        raise HTTPException(status_code=404, detail="Job not found")
        
    # Get latest logs for progress
    latest_log = db.query(database.WorkflowLog)\
        .filter(database.WorkflowLog.search_id == job_id)\
        .order_by(database.WorkflowLog.timestamp.desc())\
        .first()
        
    candidates = [
        {
            "id": r.candidate.id,
            "name": r.candidate.name,
            "headline": r.candidate.headline,
            "score": r.match_score,
            "rank": r.rank
        } for r in search.results
    ]

    return {
        "job_id": job_id,
        "status": search.status,
        "current_step": latest_log.step_name if latest_log else "queued",
        "message": latest_log.message if latest_log else "Waiting for worker...",
        "candidates": sorted(candidates, key=lambda x: x['rank'])
    }

@app.get("/candidate/{candidate_id}", response_model=dict)
async def get_candidate_detail(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(database.Candidate).filter(database.Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    return {
        "id": candidate.id,
        "name": candidate.name,
        "headline": candidate.headline,
        "location": candidate.location,
        "about": candidate.about,
        "experience": candidate.experience_raw,
        "skills": candidate.skills,
        "score": candidate.ai_fit_score,
        "github": {
            "username": candidate.github_profile.username if candidate.github_profile else None,
            "url": candidate.github_profile.url if candidate.github_profile else None
        } if candidate.github_profile else None
    }

@app.get("/report/{job_id}", response_model=dict)
async def get_search_report(job_id: str, db: Session = Depends(get_db)):
    search = db.query(database.Search).filter(database.Search.id == job_id).first()
    if not search or search.status != "completed":
        raise HTTPException(status_code=400, detail="Report not ready")
        
    return {
        "job_id": job_id,
        "summary": f"Analyzed {len(search.results)} candidates for this role.",
        "top_candidates": [r.candidate.name for r in search.results[:3]]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
