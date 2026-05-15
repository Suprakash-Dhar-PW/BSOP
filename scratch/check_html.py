import os

def check_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    print(f"File size: {len(html)} bytes")
    print(f"Contains 'listitem': {'listitem' in html}")
    print(f"Contains 'Shyamasish Mohanty': {'Shyamasish Mohanty' in html}")
    
    # Try to find the structure around Shyamasish
    index = html.find('Shyamasish Mohanty')
    if index != -1:
        print("Context around 'Shyamasish Mohanty':")
        print(html[index-500:index+500])

if __name__ == "__main__":
    check_html(r"s:\BSOP\debug\current_search.html")
