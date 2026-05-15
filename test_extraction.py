from playwright.sync_api import sync_playwright
import json
import os

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    url = f'file:///{os.path.abspath("debug/search_page.html").replace("\\\\", "/")}'
    page.goto(url)
    
    script = """() => {
        const profiles = [];
        const allLinks = Array.from(document.querySelectorAll('a[href*="/in/"]'));
        const profileMap = new Map();
        
        allLinks.forEach(link => {
            let url = link.href.split('?')[0];
            if (!url.includes('/in/')) return;
            if (url.includes('/in/search') || url.includes('/in/connections')) return;
            if (url.endsWith('/')) url = url.slice(0, -1);
            
            if (!profileMap.has(url)) {
                profileMap.set(url, { linkNodes: [] });
            }
            profileMap.get(url).linkNodes.push(link);
        });
        
        profileMap.forEach((data, url) => {
            let card = data.linkNodes[0].closest('.reusable-search__result-container, li, [role="listitem"]');
            if (!card) {
                card = data.linkNodes[0].parentElement?.parentElement?.parentElement;
            }
            if (!card) card = data.linkNodes[0].parentElement;
            
            let name = '';
            let headline = '';
            let location = '';
            
            const img = card.querySelector('img[alt]');
            if (img && img.alt && img.alt.length > 1) {
                name = img.alt;
            } else {
                for (const l of data.linkNodes) {
                    const text = l.innerText.trim();
                    if (text && text.length < 50 && !text.includes('View profile') && !text.includes('LinkedIn')) {
                        name = text.split('\\n')[0];
                        break;
                    }
                }
            }
            
            if (name && name.includes(' is open to work')) {
                name = name.replace(' is open to work', '');
            }
            
            const textElements = Array.from(card.querySelectorAll('p, .entity-result__primary-subtitle, .entity-result__secondary-subtitle, div.subline-level-1, div.subline-level-2, span'));
            
            const validTexts = textElements
                .map(el => el.innerText.trim())
                .filter(t => t.length > 5 && 
                             t !== name && 
                             !t.includes('followers') && 
                             !t.includes('connections') && 
                             !t.includes('Connect') && 
                             !t.includes('Follow') && 
                             !t.includes('Message') &&
                             !t.includes('View profile') &&
                             !t.includes('shared a post') &&
                             !t.includes('•'));
            
            const uniqueTexts = [...new Set(validTexts)];
            if (uniqueTexts.length > 0) headline = uniqueTexts[0];
            if (uniqueTexts.length > 1) location = uniqueTexts[1];
            
            if (name && (headline || url)) {
                profiles.push({ name, headline, location, profile_url: url });
            }
        });
        
        return profiles;
    }"""
    
    profiles = page.evaluate(script)
    print(json.dumps(profiles, indent=2))
    browser.close()
