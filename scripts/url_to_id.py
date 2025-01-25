import re
import requests
import sys

def extract_event_name(url:str) -> str:
    pattern = r'/event/([^/?]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_event_id(title:str) -> str:
    api_addr = 'http://gamma-api.polymarket.com/events/slug/'
    response = requests.get(api_addr + title)
    return response.json()['id']

if __name__=="__main__":
    
    if (len(sys.argv) != 2):
        print("Usage: Usage:script.py <Polymarket Vote Url>")
        exit(1)
    else:
        url = sys.argv[1] if len(sys.argv) > 1 else None
    
    get_event_id(extract_event_name(url))