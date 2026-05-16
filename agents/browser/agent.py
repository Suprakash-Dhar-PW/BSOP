import time
import random
import logging
import asyncio
from typing import Dict, Any, List, Optional
from agents.base import BaseAgent
from core.intelligence.recruiter_requirements import RecruiterRequirements
from tools.chrome_tools import ChromeMCPWrapper
from omium.tracing import trace

class BrowserAgent(BaseAgent):
    """
    Autonomous Recruiting Operations Agent.
    Executes deep entity-centric extraction and intelligence gathering.
    """
    
    def __init__(self, job_id: Optional[str] = None, db: Optional[Any] = None):
        super().__init__(name="Browser", role="Recruiting Operations", job_id=job_id, db=db)
        self.chrome = ChromeMCPWrapper()
        
    async def close(self):
        await self.chrome.close()
        
    async def run(self, requirements: RecruiterRequirements) -> List[Dict[str, Any]]:
        """
        Runs the autonomous search and extraction workflow based on recruiter requirements.
        """
        trace("Browser Intelligence Started")
        
        # 0. Initialize the browser asynchronously
        await self.chrome.start()

        # 1. Dynamic Search Strategy
        search_query = f"{requirements.role} {requirements.location}"
        if requirements.required_skills:
            search_query += f" {' '.join(requirements.required_skills[:2])}"
            
        self.log(f"Initiating autonomous candidate search: '{search_query}'", step="extraction")
        
        # 2. Execute Search
        await self.chrome.search_candidates(search_query)
        
        # 3. Extract Candidate Entities (Phase 1: Entity-Centric)
        candidates = await self.chrome.extract_profiles()
        
        if not candidates:
            self.log("No candidate entities discovered. Process halted.", level=logging.ERROR, step="extraction")
            return []
            
        # 4. Filter & Discovery Limit
        discovery_limit = requirements.max_candidates * 2
        candidates = candidates[:discovery_limit]
        
        self.log(f"Discovered {len(candidates)} entities. Starting deep profile hydration...", step="extraction")
        
        # 5. Deep Profile Hydration
        hydrated_candidates = []
        for i, candidate in enumerate(candidates):
            name = candidate.get('name', 'Unknown')
            url = candidate.get('profile_url')
            
            if not url: continue

            self.log(f"[{i+1}/{len(candidates)}] Deep-analyzing: {name}", step="extraction")
            
            # Humanoid behavior pacing
            await asyncio.sleep(random.uniform(2, 4))
            
            try:
                is_ready, readiness_score = await self.chrome.open_profile(url)
                
                if is_ready:
                    intelligence = await self.chrome.extract_candidate_intelligence()
                else:
                    self.log(f"Incomplete profile readiness for {name}. Falling back.", step="extraction")
                    intelligence = await self.chrome._stage2_light_enrichment()
                
                full_candidate = {
                    **candidate,
                    **intelligence,
                    "search_query": search_query,
                    "discovery_confidence": 0.9,
                    "readiness_score": readiness_score
                }
                hydrated_candidates.append(full_candidate)
                
            except Exception as e:
                self.log(f"Enrichment failure for {name}: {e}", level=logging.ERROR, step="extraction")
                hydrated_candidates.append({**candidate, "enrichment_failed": True})
            finally:
                await self.chrome.close_profile_page()
            
            if len(hydrated_candidates) >= requirements.max_candidates * 1.5:
                break
                
        self.log(f"Hydration complete. {len(hydrated_candidates)} entities ready for semantic scoring.", step="extraction")
        return hydrated_candidates
