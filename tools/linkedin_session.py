import os
import json
import logging
import time
from typing import Optional
from playwright.sync_api import sync_playwright, BrowserContext

logger = logging.getLogger("LinkedInSession")

class LinkedInSessionManager:
    """
    Manages LinkedIn authentication sessions and storage state.
    Ensures persistent login and session reuse to avoid repeated logins and detection.
    """
    
    def __init__(self, session_dir: str = "memory"):
        self.session_dir = session_dir
        self.session_file = os.path.join(session_dir, "linkedin_session.json")
        os.makedirs(session_dir, exist_ok=True)

    def is_session_valid(self, context: BrowserContext) -> bool:
        """Checks if the current session is still logged in."""
        page = context.new_page()
        try:
            # Navigate to a page that requires login
            page.goto("https://www.linkedin.com/feed/", wait_until="networkidle", timeout=30000)
            # Check for login elements or indicators of being logged in
            if "feed" in page.url:
                logger.info("Session is valid.")
                return True
            else:
                logger.warning("Session is invalid or expired.")
                return False
        except Exception as e:
            logger.error(f"Error checking session validity: {e}")
            return False
        finally:
            page.close()

    def login_manually(self):
        """
        Opens a browser for manual login and saves the session.
        Use this when the session expires or for the first-time setup.
        """
        logger.info("Starting manual login process...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.goto("https://www.linkedin.com/login")
            
            logger.info("Please log in manually in the browser window.")
            logger.info("Once logged in and on the feed page, the session will be saved automatically.")
            
            # Wait for user to reach the feed page
            while True:
                if "feed" in page.url:
                    time.sleep(5) # Wait for cookies to settle
                    context.storage_state(path=self.session_file)
                    logger.info(f"Session saved to {self.session_file}")
                    break
                time.sleep(2)
                if page.is_closed():
                    break
            
            browser.close()

    def get_storage_state(self) -> Optional[str]:
        """Returns the path to the storage state file if it exists."""
        if os.path.exists(self.session_file):
            return self.session_file
        return None

if __name__ == "__main__":
    # Quick CLI for manual login
    logging.basicConfig(level=logging.INFO)
    manager = LinkedInSessionManager()
    manager.login_manually()
