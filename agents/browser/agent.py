from typing import Dict, Any, List
from agents.base import BaseAgent
from tools.chrome_tools import ChromeMCPWrapper

class BrowserAgent(BaseAgent):
    """
    Browser-native operational worker.
    Uses Chrome DevTools MCP wrapper to autonomously execute web workflows.
    """
    
    def __init__(self):
        super().__init__(name="Browser", role="Digital Operations Worker")
        self.chrome = ChromeMCPWrapper()
        
    def run(self, search_query: str) -> List[Dict[str, Any]]:
        """Executes the autonomous browser workflow to find candidates."""
        self.log(f"Starting browser operations for query: '{search_query}'")
        
        # 1. Open LinkedIn
        self.log("Opening LinkedIn")
        self.chrome.open_linkedin()
        
        # 2. Search for candidates
        self.log(f"Executing search for: '{search_query}'")
        self.chrome.search_candidates(search_query)
        
        # 3. Extract profiles from search results
        self.log("Extracting candidates from search results")
        basic_profiles = self.chrome.extract_profiles()
        
        # 4. Enrich profiles with detailed extraction
        structured_candidates = []
        for profile in basic_profiles:
            self.log(f"Opening profile and extracting details for: {profile['name']}")
            self.chrome.open_profile(profile['profile_url'])
            
            details = self.chrome.extract_candidate_details(profile['name'])
            
            structured_candidate = {
                "name": profile['name'],
                "headline": profile['headline'],
                "skills": details['skills'],
                "github": details['github'],
                "location": profile['location'],
                # Keeping experience_years for downstream compatibility with ResearchAgent
                "experience_years": 5 if "Senior" in profile['headline'] else 3 
            }
            structured_candidates.append(structured_candidate)
            
        self.log(f"Returning {len(structured_candidates)} structured candidate profiles")
        return structured_candidates
