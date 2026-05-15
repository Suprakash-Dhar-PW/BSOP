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

def run_verification():
    """
    Runs the stabilization check for 4 critical roles.
    """
    roles = [
        "Frontend Engineer Bengaluru",
        "Backend Engineer Bengaluru",
        "AI Engineer Bengaluru",
        "DevOps Engineer Bengaluru"
    ]
    
    # Initialize wrapper (Headful for verification visual if needed, but here we go headless)
    # The user is a senior engineer, they want to see the JSON output.
    browser = ChromeMCPWrapper(headless=True)
    
    all_results = {}
    
    try:
        for role in roles:
            print(f"\n{'='*50}")
            print(f"VERIFYING EXTRACTION FOR: {role}")
            print(f"{'='*50}")
            
            browser.search_candidates(role)
            results = browser.extract_profiles()
            
            all_results[role] = {
                "count": len(results),
                "data": results
            }
            
            print(f"Successfully extracted {len(results)} candidates.")

        # Save final summary
        with open("verification_report.json", "w") as f:
            json.dump(all_results, f, indent=2)
        
        print("\nVerification Complete. Summary saved to 'verification_report.json'.")

    finally:
        browser.close()

if __name__ == "__main__":
    # Ensure debug directory exists
    os.makedirs("debug", exist_ok=True)
    run_verification()
