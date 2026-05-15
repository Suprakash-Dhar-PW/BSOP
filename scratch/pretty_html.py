import os

def format_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find Shyamasish Mohanty
    start = html.find('Shyamasish Mohanty')
    if start == -1:
        print("Not found")
        return
    
    # Take a chunk around it
    chunk = html[start-1000:start+2000]
    print(chunk)

if __name__ == "__main__":
    format_html(r"s:\BSOP\debug\current_search.html")
