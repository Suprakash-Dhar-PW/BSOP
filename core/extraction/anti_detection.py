import random
import time
from playwright.sync_api import BrowserContext

class AntiDetectionHardener:
    """
    Phase 7: Enterprise-grade scraping protections.
    Implements fingerprint hardening, viewport randomization, and humanized pacing.
    """
    
    @staticmethod
    def apply_stealth(context: BrowserContext):
        """Injects stealth scripts to hide Playwright presence."""
        context.add_init_script("""
            // Overwrite the 'webdriver' property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Mock Chrome runtime
            window.chrome = {
                runtime: {}
            };

            // Overwrite language and plugins
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });

            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        """)

    @staticmethod
    def randomize_viewport(page):
        width = random.randint(1280, 1920)
        height = random.randint(720, 1080)
        page.set_viewport_size({"width": width, "height": height})

    @staticmethod
    def humanized_delay(min_sec: float = 1.0, max_sec: float = 3.0):
        time.sleep(random.uniform(min_sec, max_sec))

    @staticmethod
    def humanized_scroll(page):
        for _ in range(random.randint(2, 5)):
            dist = random.randint(200, 600)
            page.evaluate(f"window.scrollBy(0, {dist})")
            time.sleep(random.uniform(0.5, 1.2))
