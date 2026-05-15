import logging
import json
import os
import sys

# Ensure local imports work
sys.path.append(os.getcwd())

from tools.chrome_tools import ChromeMCPWrapper

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

def quick_test():
    role = "Frontend Engineer Bengaluru"
    browser = ChromeMCPWrapper(headless=True)
    try:
        print(f"\nVERIFYING EXTRACTION FOR: {role}")
        browser.search_candidates(role)
        results = browser.extract_profiles()
        print(f"Extracted {len(results)} candidates.")
        print(json.dumps(results[:2], indent=2))
    finally:
        browser.close()

if __name__ == "__main__":
    quick_test()
