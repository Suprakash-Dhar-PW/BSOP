from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator

class RecruiterRequirements(BaseModel):
    """
    Phase 2: Recruiter Requirements Engine.
    Defines the criteria and weights for autonomous candidate evaluation.
    """
    role: str = Field(..., description="The target job role")
    location: str = Field("Remote", description="Preferred location")
    required_skills: List[str] = Field(default_factory=list, description="Must-have technical skills")
    preferred_companies: List[str] = Field(default_factory=list, description="Target companies (e.g. Google, Meta)")
    min_experience: int = Field(0, ge=0, description="Minimum years of experience")
    exclude_students: bool = Field(True, description="Whether to filter out students")
    exclude_interns: bool = Field(True, description="Whether to filter out interns")
    
    # Intelligence Weights (Phase 7)
    github_weight: float = Field(0.4, ge=0.0, le=1.0)
    linkedin_weight: float = Field(0.6, ge=0.0, le=1.0)
    max_candidates: int = Field(10, ge=1, le=50)
    
    # Semantic Scoring Thresholds
    min_score_threshold: float = Field(0.5, description="Minimum score to be considered 'top tier'")

    @validator('github_weight')
    def normalize_weights(cls, v, values):
        # We handle normalization logic during the ranking phase
        return v

    class Config:
        schema_extra = {
            "example": {
                "role": "Senior React Engineer",
                "location": "Bengaluru",
                "required_skills": ["React", "TypeScript", "Node.js"],
                "preferred_companies": ["Razorpay", "Zomato", "Cred"],
                "min_experience": 5,
                "github_weight": 0.5,
                "linkedin_weight": 0.5,
                "max_candidates": 10
            }
        }
