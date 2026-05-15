import logging
from abc import ABC, abstractmethod
from typing import Any

# Configure a basic logger for the platform
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)-15s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class BaseAgent(ABC):
    """
    Base class for all BSOP autonomous agents.
    Provides standardized logging, state management, and execution behavior.
    """
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.logger = logging.getLogger(self.name)
        
    def log(self, message: str, level: int = logging.INFO):
        """Standardized logging for the agent."""
        self.logger.log(level, f"[{self.role}] {message}")
        
    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """
        The core execution loop of the agent.
        Must be implemented by all subclasses.
        """
        pass
