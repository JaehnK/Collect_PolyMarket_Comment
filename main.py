import sys

import scripts.polymarket_converter as pc
import scripts.url_to_id as ui
import scripts.auto_call_api as aca

def main() -> int:
    if (len(sys.argv) != 2):
        print("Usage: Usage:script.py <Polymarket Vote Url>")
        exit(1)
    else:
        url = sys.argv[1] if len(sys.argv) > 1 else None
        
    event_name = ui.extract_event_name(url)
    event_id = ui.get_event_id(event_name)
    comments, filename = aca.fetch_all_comments(event_id)
    print(f"총 수집된 댓글 수: {len(comments)}")
    
    pc.converter(filename)


if  __name__=="__main__":
    main()