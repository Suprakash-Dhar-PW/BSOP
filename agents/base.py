import logging
from abc import ABC, abstractmethod
from typing import Any, Optional
from sqlalchemy.orm import Session
from omium.tracing import trace

class BaseAgent(ABC):
    """
    Base class for all BSOP autonomous agents.
    Provides standardized logging, state management, and execution behavior.
    """
    
    def __init__(self, name: str, role: str, job_id: Optional[str] = None, db: Optional[Session] = None):
        self.name = name
        self.role = role
        self.job_id = job_id
        self.db = db
        self.logger = logging.getLogger(self.name)
        
    def log(self, message: str, level: int = logging.INFO, step: str = None):
        """Standardized logging for the agent with DB persistence."""
        self.logger.log(level, f"[{self.role}] {message}")
        if self.db and self.job_id:
            from backend.app.models import crud
            crud.log_workflow_event(
                self.db, 
                self.job_id, 
                step=step or self.name, 
                status="running" if level == logging.INFO else "failed",
                message=message
            )
        
    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        pass
