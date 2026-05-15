from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseSourceAdapter(ABC):
    """
    Phase 8: Modular Multi-Source Intelligence Architecture.
    Base class for all talent sources (LinkedIn, GitHub, Wellfound, etc.)
    """
    
    @abstractmethod
    def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Executes a search on the source and returns basic candidate profiles."""
        pass

    @abstractmethod
    def enrich_profile(self, profile_url: str) -> Dict[str, Any]:
        """Performs deep intelligence gathering on a specific profile."""
        pass
