from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field

@dataclass
class ConfidenceValue:
    """Standardized wrapper for confidence-based extraction values."""
    value: Any
    confidence: float  # 0.0 to 1.0
    source: str       # selector | semantic | nlp | regex | inference
    raw: Optional[str] = None

@dataclass
class RecruiterRequirements:
    """
    Enterprise-grade Recruiter Intent Schema.
    Drives the RecruiterIntentEngine with dynamic role and skill synonyms.
    """
    role: str
    location: str
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    minimum_experience: int = 0
    exclude_students: bool = True
    exclude_interns: bool = True
    preferred_companies: List[str] = field(default_factory=list)
    
    # Weighting and Preferences
    github_weight: float = 0.4
    linkedin_weight: float = 0.6
    max_candidates: int = 10
    
    # Dynamic Semantic Context (Populated by ExecutiveAgent)
    role_synonyms: List[str] = field(default_factory=list)
    skill_synonyms: Dict[str, List[str]] = field(default_factory=dict)
    
    def __post_init__(self):
        # Basic constraints
        self.minimum_experience = max(0, self.minimum_experience)
        self.max_candidates = max(1, self.max_candidates)
        
        # Normalize weights
        total = self.github_weight + self.linkedin_weight
        if total > 0:
            self.github_weight /= total
            self.linkedin_weight /= total
            
    def get_full_target_skills(self) -> List[str]:
        """Returns all skills including synonyms for semantic matching."""
        all_skills = set(self.required_skills + self.preferred_skills)
        for synonyms in self.skill_synonyms.values():
            all_skills.update(synonyms)
        return list(all_skills)

    def get_all_role_keywords(self) -> List[str]:
        """Returns role and its synonyms."""
        return list(set([self.role] + self.role_synonyms))
