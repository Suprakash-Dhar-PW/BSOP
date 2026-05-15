from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class RecruiterQuery(Base):
    __tablename__ = "recruiter_queries"
    
    id = Column(Integer, primary_key=True)
    raw_query = Column(Text, nullable=False)
    parsed_intent = Column(JSON) # Structured intent from LLM
    created_at = Column(DateTime, default=datetime.utcnow)
    
    searches = relationship("Search", back_populates="query")

class Search(Base):
    __tablename__ = "searches"
    
    id = Column(String, primary_key=True) # Job ID / UUID
    query_id = Column(Integer, ForeignKey("recruiter_queries.id"))
    status = Column(String) # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    query = relationship("RecruiterQuery", back_populates="searches")
    results = relationship("SearchResult", back_populates="search")
    logs = relationship("WorkflowLog", back_populates="search")

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    profile_url = Column(String, unique=True, nullable=False)
    headline = Column(Text)
    location = Column(String)
    
    # Enrichment data
    about = Column(Text)
    experience_raw = Column(Text)
    skills = Column(JSON) # List of strings
    
    # Intelligence scores
    ai_fit_score = Column(Float)
    semantic_analysis = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    search_results = relationship("SearchResult", back_populates="candidate")
    github_profile = relationship("GitHubProfile", back_populates="candidate", uselist=False)

class SearchResult(Base):
    __tablename__ = "search_results"
    
    id = Column(Integer, primary_key=True)
    search_id = Column(String, ForeignKey("searches.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    rank = Column(Integer)
    match_score = Column(Float)
    
    search = relationship("Search", back_populates="results")
    candidate = relationship("Candidate", back_populates="search_results")

class GitHubProfile(Base):
    __tablename__ = "github_profiles"
    
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    username = Column(String)
    url = Column(String)
    public_repos = Column(Integer)
    top_languages = Column(JSON)
    intelligence_summary = Column(Text)
    
    candidate = relationship("Candidate", back_populates="github_profile")

class WorkflowLog(Base):
    __tablename__ = "workflow_logs"
    
    id = Column(Integer, primary_key=True)
    search_id = Column(String, ForeignKey("searches.id"))
    step_name = Column(String) # extraction, hydration, ranking
    status = Column(String)
    message = Column(Text)
    payload = Column(JSON) # Debug info
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    search = relationship("Search", back_populates="logs")
