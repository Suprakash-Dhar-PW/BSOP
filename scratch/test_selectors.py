from bs4 import BeautifulSoup
import json
import os

def test_selectors(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # New proposed selectors
    candidate_cards = soup.select('div[role="listitem"]')
    print(f"Found {len(candidate_cards)} candidate cards.")
    
    results = []
    for i, card in enumerate(candidate_cards):
        # Name and Profile URL
        profile_link = card.select_one('a[href*="/in/"]')
        name = profile_link.get_text(strip=True) if profile_link else "N/A"
        url = profile_link['href'] if profile_link else "N/A"
        
        # Headline and Location
        # In the HTML, headline is in a span inside a p inside a div
        # Location is in a span inside a p inside a div
        spans = card.select('p > span')
        # Filter spans to find headline and location
        # The name p also has spans (verified etc)
        # Let's try to find spans that are children of divs
        div_spans = card.select('div p span')
        
        headline = div_spans[0].get_text(strip=True) if len(div_spans) > 0 else "N/A"
        location = div_spans[1].get_text(strip=True) if len(div_spans) > 1 else "N/A"
        
        # Clean up name (LinkedIn adds 'Verified' or '• 2nd' text)
        if " • " in name:
            name = name.split(" • ")[0]
        if "Verified" in name:
            name = name.replace("Verified", "").strip()

        results.append({
            "index": i + 1,
            "name": name,
            "headline": headline,
            "location": location,
            "url": url
        })
    
    return results

if __name__ == "__main__":
    html_file = r"s:\BSOP\debug\extraction_1778872166.html"
    if os.path.exists(html_file):
        results = test_selectors(html_file)
        print(json.dumps(results, indent=2))
    else:
        print(f"File {html_file} not found.")
