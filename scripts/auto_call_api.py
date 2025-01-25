import argparse
import requests
import time
import json
from typing import List, Dict, Any
import re
import sys

def extract_event_name(url:str) -> str:
    pattern = r'/event/([^/?]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_event_id(title:str) -> str:
    api_addr = 'http://gamma-api.polymarket.com/events/slug/'
    response = requests.get(api_addr + title)
    return (response.json()['id'])

def fetch_all_comments(event_id: str, batch_size: int = 10) -> List[Dict[Any, Any]]:
    """
    Polymarket의 모든 댓글을 수집하는 함수
    
    Args:
        event_id: 이벤트 ID
        batch_size: 한 번에 가져올 댓글 수
    
    Returns:
        수집된 모든 댓글 리스트
    """
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
        'Origin': 'https://polymarket.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }

    base_params = {
        'parent_entity_type': 'Event',
        'parent_entity_id': event_id,
        'get_positions': 'true',
        'get_reports': 'true',
        'ascending': 'false',
        'order': 'createdAt',
        'holders_only': 'true',
    }

    all_comments = []
    offset = 0
    
    while True:
        params = {
            **base_params,
            'limit': str(batch_size),
            'offset': str(offset)
        }
        
        try:
            response = requests.get(
                'https://gamma-api.polymarket.com/comments',
                params=params,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            
            if not data:
                break
                
            all_comments.extend(data)
            print(f"수집된 댓글 수: {len(all_comments)}")
            
            if len(data) < batch_size:
                break

            offset += batch_size
            time.sleep(3)
            
        except requests.exceptions.RequestException as e:
            print(f"에러 발생: {e}")
            save_comments(all_comments, event_id)
            raise
            
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 에러: {e}")
            save_comments(all_comments, event_id)
            raise
            
    filename = save_comments(all_comments, event_id)
    return all_comments, filename

def save_comments(comments: List[Dict[Any, Any]], event_id: str) -> str:
    """수집된 댓글을 JSON 파일로 저장"""
    filename = f"polymarket_comments_{event_id}_{len(comments)}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)
    print(f"댓글이 {filename}에 저장되었습니다.")
    return filename

def main() -> int:
    if (len(sys.argv) != 2):
        print("Usage: Usage: python auto_call_api.py <Polymarket Vote Url>")
        exit(1)
    else:
        url = sys.argv[1] if len(sys.argv) > 1 else None
    
    name = extract_event_name(url)
    event_id = str(get_event_id(name))
    comments = fetch_all_comments("17104")
    print(f"총 수집된 댓글 수: {len(comments)}")

if __name__ == "__main__":
    main()