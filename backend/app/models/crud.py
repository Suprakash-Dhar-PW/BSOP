from sqlalchemy.orm import Session
from .database import Search, Candidate, SearchResult, WorkflowLog, RecruiterQuery
from datetime import datetime
import json

def create_search_job(db: Session, job_id: str, raw_query: str):
    # 1. Create Query record
    query = RecruiterQuery(raw_query=raw_query)
    db.add(query)
    db.flush()
    
    # 2. Create Search record
    search = Search(id=job_id, query_id=query.id, status="queued")
    db.add(search)
    db.commit()
    return search

def update_search_status(db: Session, job_id: str, status: str):
    search = db.query(Search).filter(Search.id == job_id).first()
    if search:
        search.status = status
        search.updated_at = datetime.utcnow()
        db.commit()

def log_workflow_event(db: Session, job_id: str, step: str, status: str, message: str, payload: dict = None):
    log = WorkflowLog(
        search_id=job_id,
        step_name=step,
        status=status,
        message=message,
        payload=payload
    )
    db.add(log)
    db.commit()

def save_candidate_result(db: Session, job_id: str, candidate_data: dict, rank: int):
    # Check if candidate exists by URL
    candidate = db.query(Candidate).filter(Candidate.profile_url == candidate_data['profile_url']).first()
    if not candidate:
        candidate = Candidate(
            name=candidate_data['name'],
            profile_url=candidate_data['profile_url'],
            headline=candidate_data.get('headline'),
            location=candidate_data.get('location'),
            skills=candidate_data.get('skills', []),
            ai_fit_score=candidate_data.get('final_score', 0)
        )
        db.add(candidate)
        db.flush()
    
    # Create result link
    result = SearchResult(
        search_id=job_id,
        candidate_id=candidate.id,
        rank=rank,
        match_score=candidate_data.get('final_score', 0)
    )
    db.add(result)
    db.commit()
