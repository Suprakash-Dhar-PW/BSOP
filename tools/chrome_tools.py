import logging
import time
from typing import Dict, Any, List

from config.selectors import LINKEDIN_SELECTORS

logger = logging.getLogger("ChromeTools")

class ChromeMCPWrapper:
    """
    Wrapper for Chrome DevTools MCP server.
    Encapsulates all browser operations and provides a clean, 
    reusable tool layer for autonomous browser agents.
    Designed to easily scale for CRM, procurement, or support workflows.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("[Digital Operations Worker]")
        self.mode = "mock"
        # In a fully integrated environment, this would initialize an MCP client
        # Example: self.client = mcp.Client(server_name="chrome-devtools-mcp")
        
    def _execute_mcp_tool(self, tool_name: str, params: Dict[str, Any] = None) -> Any:
        """
        Core method to dispatch MCP tools.
        Abstracts the underlying protocol from the business logic methods.
        """
        params_str = str(params)
        if len(params_str) > 100:
            params_str = params_str[:97] + "..."
            
        self.logger.info(f"[Chrome MCP] Executing {tool_name} | Params: {params_str}")
        time.sleep(1) # Simulate network and execution delay
        
        # Placeholder for actual MCP client execution
        if self.mode == "mock":
            return {"status": "success"}
        elif self.mode == "mcp":
            raise NotImplementedError("Real MCP execution not yet implemented")
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

    def open_linkedin(self):
        """Navigates to the LinkedIn search page."""
        self._execute_mcp_tool("mcp_chrome-devtools-mcp_navigate_page", {
            "url": "https://www.linkedin.com"
        })
        self._execute_mcp_tool("mcp_chrome-devtools-mcp_wait_for", {
            "text": ["LinkedIn", "Sign in"]
        })

    def search_candidates(self, query: str):
        """Executes a search query on LinkedIn."""
        # Convert query to URL encoding for the search
        encoded_query = query.replace(' ', '%20')
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={encoded_query}"
        
        self._execute_mcp_tool("mcp_chrome-devtools-mcp_navigate_page", {
            "url": search_url
        })
        self._execute_mcp_tool("mcp_chrome-devtools-mcp_wait_for", {
            "text": ["People", "Results"]
        })

    def extract_profiles(self) -> List[Dict[str, Any]]:
        """Extracts candidate profile links and basic data from search results."""
        # We use evaluate_script to extract structured data via JS
        script = f"""() => {{
            const profiles = [];
            document.querySelectorAll('{LINKEDIN_SELECTORS["profile_card"]}').forEach(el => {{
                const nameEl = el.querySelector('{LINKEDIN_SELECTORS["name"]}');
                const titleEl = el.querySelector('{LINKEDIN_SELECTORS["headline"]}');
                const locationEl = el.querySelector('{LINKEDIN_SELECTORS["location"]}');
                const linkEl = el.querySelector('{LINKEDIN_SELECTORS["profile_link"]}');
                
                if (nameEl && titleEl) {{
                    profiles.push({{
                        name: nameEl.innerText.trim(),
                        headline: titleEl.innerText.trim(),
                        location: locationEl ? locationEl.innerText.trim() : "",
                        profile_url: linkEl ? linkEl.href : ""
                    }});
                }}
            }});
            return profiles;
        }}"""
        self._execute_mcp_tool("mcp_chrome-devtools-mcp_evaluate_script", {"function": script})
        
        # For Phase 2, returning structured mock data simulating the extraction
        return [
            {
                "name": "Aarav Sharma",
                "headline": "Senior Frontend Engineer | React | Next.js",
                "location": "Bengaluru",
                "profile_url": "https://linkedin.com/in/aaravsharma"
            },
            {
                "name": "Priya Patel",
                "headline": "Frontend Developer @ TechCorp",
                "location": "Bengaluru, Karnataka, India",
                "profile_url": "https://linkedin.com/in/priyapatel"
            }
        ]

    def open_profile(self, profile_url: str):
        """Navigates to a specific candidate's profile."""
        self._execute_mcp_tool("mcp_chrome-devtools-mcp_navigate_page", {"url": profile_url})
        self._execute_mcp_tool("mcp_chrome-devtools-mcp_wait_for", {"text": ["Experience", "Skills", "Education"]})

    def extract_candidate_details(self, name: str) -> Dict[str, Any]:
        """Extracts detailed information from a candidate's profile page."""
        script = f"""() => {{
            const skills = Array.from(document.querySelectorAll('{LINKEDIN_SELECTORS["skills"]}')).map(el => el.innerText.trim());
            const githubLink = document.querySelector('a[href*="github.com"]');
            return {{
                skills: skills,
                github: githubLink ? githubLink.href : null
            }};
        }}"""
        self._execute_mcp_tool("mcp_chrome-devtools-mcp_evaluate_script", {"function": script})
        
        # Mock detailed extraction mapping to the extracted name
        return {
            "skills": ["React", "NextJS", "TypeScript", "Tailwind CSS"],
            "github": f"https://github.com/{name.replace(' ', '').lower()}"
        }
