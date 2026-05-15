import os
import json
import logging
import random
import time
import re
from typing import Dict, Any, List, Optional, Tuple, Union
from playwright.sync_api import sync_playwright, Page, BrowserContext, Browser
from tools.linkedin_session import LinkedInSessionManager
from config.selectors import LINKEDIN_SELECTORS

logger = logging.getLogger("ChromeTools")

class LinkedInValidator:
    """Utility for cleaning and validating extracted LinkedIn entities."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        if not text: return ""
        # Take only the first line to avoid capturing child element text
        text = text.split('\n')[0].strip()
        # Remove degree symbols (2nd, 3rd+), mutual connection counts, etc.
        text = re.sub(r'[•·].*', '', text)
        text = text.replace("Verified", "")
        return text.strip()

    @staticmethod
    def is_valid_profile_url(url: str) -> bool:
        if not url: return False
        return "/in/" in url and "search" not in url.lower()

class ChromeMCPWrapper:
    """
    Production-grade LinkedIn Extraction Engine.
    Implements session persistence, crash recovery, stealth, and human-like automation.
    """
    
    def __init__(self, headless: bool = True):
        self.logger = logging.getLogger("[ChromeTools]")
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.session_manager = LinkedInSessionManager()
        self._start_browser()

    def _start_browser(self):
        """Starts Playwright with anti-detection and session management."""
        try:
            if self.playwright:
                self.close()
            
            self.playwright = sync_playwright().start()
            
            launch_args = [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
                "--window-position=0,0",
                "--ignore-certificate-errors",
                "--disable-setuid-sandbox",
            ]
            
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=launch_args
            )
            
            storage_state = self.session_manager.get_storage_state()
            
            self.context = self.browser.new_context(
                storage_state=storage_state,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1440, "height": 900},
                device_scale_factor=1,
            )
            
            # Anti-detection stealth scripts
            self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = { runtime: {} };
            """)
            
            self.page = self.context.new_page()
            os.makedirs("debug", exist_ok=True)
            self.logger.info("Browser initialized with session persistence.")
            
        except Exception as e:
            self.logger.error(f"Critical browser startup failure: {e}")
            raise

    def ensure_active(self):
        """Ensures the browser session is active and page is responsive."""
        try:
            if not self.browser or not self.page or self.page.is_closed():
                self.logger.warning("Browser or page lost. Recovering...")
                self._start_browser()
            # Test connectivity
            self.page.evaluate("1")
        except Exception:
            self.logger.warning("Page unresponsive. Restarting...")
            self._start_browser()

    def close(self):
        """Robust cleanup of Playwright resources."""
        try:
            if self.page: self.page.close()
            if self.context: self.context.close()
            if self.browser: self.browser.close()
            if self.playwright: self.playwright.stop()
        except Exception as e:
            self.logger.debug(f"Cleanup error (likely connection closed): {e}")
        finally:
            self.page = self.context = self.browser = self.playwright = None

    # =====================================================
    # HUMAN-LIKE INTERACTIONS
    # =====================================================

    def human_delay(self, min_s=1.0, max_s=3.0):
        time.sleep(random.uniform(min_s, max_s))

    def human_type(self, selector: str, text: str):
        self.ensure_active()
        self.page.wait_for_selector(selector)
        self.page.click(selector)
        for char in text:
            self.page.type(selector, char, delay=random.randint(50, 150))
        self.human_delay(0.5, 1.0)

    def human_scroll(self):
        self.ensure_active()
        scroll_dist = random.randint(300, 700)
        self.page.evaluate(f"window.scrollBy({{top: {scroll_dist}, behavior: 'smooth'}})")
        self.human_delay(1.0, 2.0)

    # =====================================================
    # EXTRACTION CORE
    # =====================================================

    def search_candidates(self, keywords: str, max_retries=3):
        for attempt in range(max_retries):
            try:
                self.ensure_active()
                self.logger.info(f"Searching: {keywords} (Attempt {attempt+1})")
                url = f"https://www.linkedin.com/search/results/people/?keywords={keywords.replace(' ', '%20')}"
                
                self.page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Check for login wall
                if "login" in self.page.url or "checkpoint" in self.page.url:
                    self.logger.error("Session expired or security checkpoint reached.")
                    return False

                # Hydrate results
                self._hydrate_results()
                return True
            except Exception as e:
                self.logger.error(f"Search attempt {attempt+1} failed: {e}")
                self.human_delay(2, 5)
                self._start_browser() # Recovery
        return False

    def _hydrate_results(self):
        """Scrolls and stabilizes the results page."""
        self.logger.info("Hydrating results...")
        for _ in range(random.randint(2, 4)):
            self.human_scroll()
        time.sleep(2)

    def extract_profiles(self) -> List[Dict[str, Any]]:
        """
        Entity-Centric Extraction.
        Extracts candidate data by identifying profile links and traversing the DOM.
        """
        self.ensure_active()
        self.logger.info("Executing entity-centric extraction...")
        
        try:
            # 1. Capture all candidate links
            all_links = self.page.query_selector_all('a[href*="/in/"]')
            candidates_map = {}
            
            for link in all_links:
                try:
                    href = link.get_attribute("href")
                    if not href: continue
                    
                    profile_url = href.split('?')[0]
                    if not profile_url.startswith('http'):
                        profile_url = f"https://www.linkedin.com{profile_url}"
                    
                    if not LinkedInValidator.is_valid_profile_url(profile_url) or profile_url in candidates_map:
                        continue
                    
                    # Get the card container
                    container = link.evaluate_handle("""
                        el => {
                            let curr = el;
                            for (let i=0; i<10; i++) {
                                if (!curr.parentElement) break;
                                curr = curr.parentElement;
                                if (curr.tagName === 'LI' || curr.classList.contains('entity-result')) return curr;
                            }
                            return curr;
                        }
                    """)
                    
                    text = container.evaluate("el => el.innerText")
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    
                    if not lines: continue
                    
                    # Simple inference
                    name = lines[0]
                    headline = lines[1] if len(lines) > 1 else ""
                    
                    # Filter ads
                    if any(noise in text.lower() for noise in ["promoted", "suggested", "ads by"]):
                        continue

                    if "LinkedIn Member" in name: continue

                    candidates_map[profile_url] = {
                        "name": LinkedInValidator.clean_text(name),
                        "headline": LinkedInValidator.clean_text(headline),
                        "profile_url": profile_url,
                        "location": self._infer_location(lines),
                        "discovery_confidence": 0.9
                    }
                except:
                    continue
            
            candidates = list(candidates_map.values())
            self.save_debug_snapshots(candidates)
            self.logger.info(f"Extracted {len(candidates)} unique candidates.")
            return candidates
            
        except Exception as e:
            self.logger.error(f"Extraction failed: {e}")
            return []

    def _infer_location(self, lines: List[str]) -> str:
        for line in lines[2:6]:
            if any(t in line.lower() for t in ["india", "remote", "area", "united", "san", "london", "bangalore"]):
                return line
        return lines[2] if len(lines) > 2 else "Unknown"

    def open_profile(self, url: str) -> Tuple[bool, float]:
        try:
            self.ensure_active()
            self.page.goto(url, wait_until="load", timeout=30000)
            self.human_delay(1, 3)
            # Scroll a bit to trigger lazy loading of sections
            self.human_scroll()
            
            try:
                self.page.wait_for_selector(".pv-top-card, #about", timeout=5000)
                return True, 100.0
            except:
                return False, 50.0
        except Exception as e:
            self.logger.error(f"Error opening profile {url}: {e}")
            return False, 0.0

    def extract_candidate_intelligence(self) -> Dict[str, Any]:
        """Deep profile extraction."""
        try:
            self.ensure_active()
            about = self.page.query_selector("#about, .pv-about-section")
            experience = self.page.query_selector("#experience, .pv-experience-section")
            
            return {
                "about": about.inner_text() if about else "",
                "experience_raw": experience.inner_text() if experience else "",
                "extraction_confidence": 90.0,
                "profile_enrichment_failed": False
            }
        except:
            return {"profile_enrichment_failed": True}

    def close_profile_page(self):
        pass

    def save_debug_snapshots(self, data: List[Dict[str, Any]]):
        ts = int(time.time())
        try:
            self.page.screenshot(path=f"debug/extraction_{ts}.png")
            with open(f"debug/extraction_{ts}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except:
            pass
