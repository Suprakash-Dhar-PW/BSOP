import os
import json
import time
import random
import logging
from typing import List, Dict, Any, Optional
from playwright.sync_api import Page, ElementHandle

logger = logging.getLogger("LinkedInExtractor")

class LinkedInExtractor:
    """
    Phase 1: Stabilized LinkedIn Extraction Engine.
    Implements card-first extraction, robust hydration, and validation.
    """
    
    def __init__(self, page: Page, debug_dir: str = "debug"):
        self.page = page
        self.debug_dir = debug_dir
        os.makedirs(self.debug_dir, exist_ok=True)
        
    def hydrate_page(self):
        """
        Implements intelligent scrolling and React hydration stabilization.
        """
        logger.info("Starting page hydration...")
        
        # Initial scroll to trigger lazy loads
        for i in range(3):
            scroll_dist = random.randint(700, 1000)
            self.page.evaluate(f"window.scrollBy(0, {scroll_dist})")
            time.sleep(random.uniform(0.8, 1.5))
            
        # Wait for the specific "wait" period requested in Phase 1
        logger.info("Hydration: Waiting 5 seconds for React components to stabilize...")
        time.sleep(5)
        
        # Final scroll back to top to ensure we didn't miss anything (optional but good for visibility)
        self.page.evaluate("window.scrollTo(0, 0)")
        
    def save_debug_state(self, suffix: str = ""):
        """Saves HTML and screenshots for debugging."""
        timestamp = int(time.time())
        tag = f"{timestamp}_{suffix}"
        
        try:
            self.page.screenshot(path=os.path.join(self.debug_dir, f"extraction_{tag}.png"))
            with open(os.path.join(self.debug_dir, f"extraction_{tag}.html"), "w", encoding="utf-8") as f:
                f.write(self.page.content())
        except Exception as e:
            logger.error(f"Failed to save debug state: {e}")

    def extract_candidates(self) -> List[Dict[str, Any]]:
        """
        Iterates card-by-card to extract candidate info.
        """
        self.hydrate_page()
        self.save_debug_state("before_extraction")
        
        # Robust card selectors
        CARD_SELECTOR = ".reusable-search__result-container, li.reusable-search__result-container, [data-view-name='search-entity-result-universal-template']"
        
        cards = self.page.query_selector_all(CARD_SELECTOR)
        logger.info(f"Found {len(cards)} candidate cards.")
        
        candidates = []
        for i, card in enumerate(cards):
            try:
                candidate = self._extract_card(card)
                if candidate and self._validate_candidate(candidate):
                    candidates.append(candidate)
            except Exception as e:
                logger.error(f"Error extracting card {i}: {e}")
                
        # Deduplicate
        seen_urls = set()
        unique_candidates = []
        for c in candidates:
            if c['profile_url'] not in seen_urls:
                unique_candidates.append(c)
                seen_urls.add(c['profile_url'])
        
        logger.info(f"Extracted {len(unique_candidates)} unique validated candidates.")
        
        # Save raw JSON results
        with open(os.path.join(self.debug_dir, f"raw_extraction_{int(time.time())}.json"), "w", encoding="utf-8") as f:
            json.dump(unique_candidates, f, indent=2)
            
        return unique_candidates

    def _extract_card(self, card: ElementHandle) -> Optional[Dict[str, Any]]:
        """
        Extracts data from a single LinkedIn card.
        """
        # Name: Usually inside a link with /in/
        name_el = card.query_selector("span[aria-hidden='true'], .entity-result__title-text a")
        name = name_el.inner_text().split('\n')[0].strip() if name_el else ""
        
        # Profile URL
        url_el = card.query_selector("a[href*='/in/']")
        profile_url = url_el.get_attribute("href").split('?')[0] if url_el else ""
        if profile_url and profile_url.endswith('/'):
            profile_url = profile_url[:-1]
            
        # Headline
        headline_el = card.query_selector(".entity-result__primary-subtitle, .t-14.t-black.t-normal")
        headline = headline_el.inner_text().strip() if headline_el else ""
        
        # Location
        location_el = card.query_selector(".entity-result__secondary-subtitle, .t-12.t-black--light.t-normal")
        location = location_el.inner_text().strip() if location_el else ""
        
        # Clean name if it contains "Degree" or other noise
        if " • " in name:
            name = name.split(" • ")[0]
            
        return {
            "name": name,
            "headline": headline,
            "location": location,
            "profile_url": profile_url
        }

    def _validate_candidate(self, candidate: Dict[str, Any]) -> bool:
        """
        Validates the extracted candidate data.
        """
        if not candidate['name'] or len(candidate['name']) < 2:
            return False
        if not candidate['profile_url'] or "/in/" not in candidate['profile_url']:
            return False
        # Remove garbage entities (e.g. "LinkedIn Member")
        if "LinkedIn Member" in candidate['name']:
            return False
        return True
