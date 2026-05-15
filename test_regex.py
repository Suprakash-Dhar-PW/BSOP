import re

with open('debug/search_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Instead of parsing the DOM, let's just see if we can find any class for listitem:
listitems = re.findall(r'<[^>]*role="listitem"[^>]*>', html)
print('Number of role=listitem:', len(listitems))

if len(listitems) == 0:
    lis = re.findall(r'<li[^>]*>', html)
    print('Number of <li>:', len(lis))

