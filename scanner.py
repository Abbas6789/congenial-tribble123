import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_history_endpoints(target_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(target_url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = [script.get('src') for script in soup.find_all('script') if script.get('src')]
        
        keywords = ['history', 'stats', 'results', 'v1/crash']
        found = []
        for s in scripts:
            for k in keywords:
                if k in s.lower(): found.append(urljoin(target_url, s))
        
        return found if found else "لنک نہیں ملا، مینوئل ڈیٹا ڈالیں۔"
    except:
        return "سائٹ تک رسائی ممکن نہیں۔"
