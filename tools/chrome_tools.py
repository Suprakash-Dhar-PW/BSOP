import os
import json
import logging
import random
import asyncio
import re
from typing import Dict, Any, List, Optional, Tuple, Union
from playwright.async_api import async_playwright, Page, BrowserContext, Browser
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

    async def start(self):
        """Starts Playwright with anti-detection and session management."""
        try:
            if self.playwright:
                await self.close()
            
            playwright_mgr = async_playwright()
            self.playwright = await playwright_mgr.start()
            
            launch_args = [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
                "--window-position=0,0",
                "--ignore-certificate-errors",
                "--disable-setuid-sandbox",
            ]
            
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=launch_args
            )
            
            storage_state = self.session_manager.get_storage_state()
            
            self.context = await self.browser.new_context(
                storage_state=storage_state,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1440, "height": 900},
                device_scale_factor=1,
            )
            
            # Anti-detection stealth scripts
            await self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = { runtime: {} };
            """)
            
            self.page = await self.context.new_page()
            os.makedirs("debug", exist_ok=True)
            self.logger.info("Browser initialized with session persistence.")
            
        except Exception as e:
            self.logger.error(f"Critical browser startup failure: {e}")
            raise

    async def ensure_active(self):
        """Ensures the browser session is active and page is responsive."""
        try:
            if not self.browser or not self.page or self.page.is_closed():
                self.logger.warning("Browser or page lost. Recovering...")
                await self.start()
            # Test connectivity
            await self.page.evaluate("1")
        except Exception:
            self.logger.warning("Page unresponsive. Restarting...")
            await self.start()

    async def close(self):
        """Robust cleanup of Playwright resources."""
        try:
            if self.page: await self.page.close()
            if self.context: await self.context.close()
            if self.browser: await self.browser.close()
            if self.playwright: await self.playwright.stop()
        except Exception as e:
            self.logger.debug(f"Cleanup error (likely connection closed): {e}")
        finally:
            self.page = self.context = self.browser = self.playwright = None

    # =====================================================
    # HUMAN-LIKE INTERACTIONS
    # =====================================================

    async def human_delay(self, min_s=1.0, max_s=3.0):
        await asyncio.sleep(random.uniform(min_s, max_s))

    async def human_type(self, selector: str, text: str):
        await self.ensure_active()
        await self.page.wait_for_selector(selector)
        await self.page.click(selector)
        for char in text:
            await self.page.type(selector, char, delay=random.randint(50, 150))
        await self.human_delay(0.5, 1.0)

    async def human_scroll(self):
        await self.ensure_active()
        scroll_dist = random.randint(300, 700)
        await self.page.evaluate(f"window.scrollBy({{top: {scroll_dist}, behavior: 'smooth'}})")
        await self.human_delay(1.0, 2.0)

    # =====================================================
    # EXTRACTION CORE
    # =====================================================

    async def search_candidates(self, keywords: str, max_retries=3):
        for attempt in range(max_retries):
            try:
                await self.ensure_active()
                self.logger.info(f"Searching: {keywords} (Attempt {attempt+1})")
                url = f"https://www.linkedin.com/search/results/people/?keywords={keywords.replace(' ', '%20')}"
                
                await self.page.goto(url, wait_until="load", timeout=60000)
                
                # Check for login wall
                if "login" in self.page.url or "checkpoint" in self.page.url:
                    self.logger.error("Session expired or security checkpoint reached.")
                    return False

                # Hydrate results
                await self._hydrate_results()
                return True
            except Exception as e:
                self.logger.error(f"Search attempt {attempt+1} failed: {e}")
                await self.human_delay(2, 5)
                await self.start() # Recovery
        return False

    async def _hydrate_results(self):
        """Scrolls and stabilizes the results page."""
        self.logger.info("Hydrating results...")
        for _ in range(random.randint(2, 4)):
            await self.human_scroll()
        await asyncio.sleep(2)

    async def extract_profiles(self) -> List[Dict[str, Any]]:
        """
        Entity-Centric Extraction.
        Extracts candidate data by identifying profile links and traversing the DOM.
        """
        await self.ensure_active()
        self.logger.info("Executing entity-centric extraction...")
        
        try:
            # 1. Capture all candidate links
            all_links = await self.page.query_selector_all('a[href*="/in/"]')
            candidates_map = {}
            
            for link in all_links:
                try:
                    href = await link.get_attribute("href")
                    if not href: continue
                    
                    profile_url = href.split('?')[0]
                    if not profile_url.startswith('http'):
                        profile_url = f"https://www.linkedin.com{profile_url}"
                    
                    if not LinkedInValidator.is_valid_profile_url(profile_url) or profile_url in candidates_map:
                        continue
                    
                    # Get the card container
                    container = await link.evaluate_handle("""
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
                    
                    text = await container.evaluate("el => el.innerText")
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
            await self.save_debug_snapshots(candidates)
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

    async def open_profile(self, url: str) -> Tuple[bool, float]:
        try:
            await self.ensure_active()
            await self.page.goto(url, wait_until="load", timeout=30000)
            await self.human_delay(1, 3)
            # Scroll a bit to trigger lazy loading of sections
            await self.human_scroll()
            
            try:
                await self.page.wait_for_selector(".pv-top-card, #about", timeout=5000)
                return True, 100.0
            except:
                return False, 50.0
        except Exception as e:
            self.logger.error(f"Error opening profile {url}: {e}")
            return False, 0.0

    async def extract_candidate_intelligence(self) -> Dict[str, Any]:
        """Deep profile extraction."""
        try:
            await self.ensure_active()
            about = await self.page.query_selector("#about, .pv-about-section")
            experience = await self.page.query_selector("#experience, .pv-experience-section")
            
            return {
                "about": await about.inner_text() if about else "",
                "experience_raw": await experience.inner_text() if experience else "",
                "extraction_confidence": 90.0,
                "profile_enrichment_failed": False
            }
        except:
            return {"profile_enrichment_failed": True}

    async def _stage2_light_enrichment(self) -> Dict[str, Any]:
        """Light profile extraction when full enrichment fails."""
        try:
            await self.ensure_active()
            about = await self.page.query_selector(".pv-about-section")
            return {
                "about": await about.inner_text() if about else "",
                "extraction_confidence": 50.0,
                "profile_enrichment_failed": False
            }
        except:
            return {"profile_enrichment_failed": True}

    async def close_profile_page(self):
        pass

    async def save_debug_snapshots(self, data: List[Dict[str, Any]]):
        import time
        ts = int(time.time())
        try:
            await self.page.screenshot(path=f"debug/extraction_{ts}.png")
            with open(f"debug/extraction_{ts}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except:
            pass
