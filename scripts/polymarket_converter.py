import json
from typing import List, Dict, Any
import sys
import re
import pandas as pd
import numpy as np

def print_json_structure(data: Any, indent: str = '', prefix: str = 'ROOT'):
    """JSON 데이터의 구조를 트리 형식으로 출력"""
    if isinstance(data, dict):
        print(f"{indent}{prefix} (dict):")
        for key, value in data.items():
            print_json_structure(value, indent + '    ', key)
    elif isinstance(data, list):
        print(f"{indent}{prefix} (list, length={len(data)}):")
        if data:  # 리스트가 비어있지 않은 경우
            # 첫 번째 항목의 구조만 보여줌
            print_json_structure(data[0], indent + '    ', 'item[0]')
    else:
        print(f"{indent}{prefix}: {type(data).__name__} = {str(data)[:50]}")

def OpenJsonVisualisation(path: str) -> pd.DataFrame:
    with open(path) as f:
        data = json.load(f)
    print("\n=== JSON 구조 분석 ===")
    print_json_structure(data)
    print("=== 구조 분석 끝 ===\n")
    df = pd.DataFrame(data)
    return df

def MainVisualisation(path: str) -> int:
    try:
        df = OpenJson(path)
        print("데이터 로드 완료")
        print(f"데이터 크기: {df.shape}")
        print("\n처음 5개 행:")
        print(df.head())
        df.to_csv(path[:-4]+"csv", encoding="utf-8-sig")
        return 0
    except FileNotFoundError:
        print(f"오류: {path} 파일을 찾을 수 없습니다.")
        return 1
    except json.JSONDecodeError:
        print("오류: JSON 파일 형식이 잘못되었습니다.")
        return 1
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return 1

def flatten_positions(positions: List[Dict[str, Any]]) -> Dict[str, str]:
    """positions 리스트에서 첫 번째 position의 정보를 평탄화된 딕셔너리로 변환"""
    if not positions:
        return {
            'position_tokenId': '',
            'position_size': ''
        }
    
    position = positions[0]  # 첫 번째 position 사용
    return {
        'position_tokenId': position.get('tokenId', ''),
        'position_size': position.get('positionSize', '')
    }

def OpenJson(path: str) -> pd.DataFrame:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 각 레코드를 평탄화된 형태로 변환
    flattened_data = []
    for record in data:
        flat_record = {}
        
        # profile과 positions 처리
        if 'profile' in record:
            profile = record['profile']
            positions = profile.get('positions', [])
            
            # positions 평탄화
            position_data = flatten_positions(positions)
            
            # profile의 다른 필드들 복사
            for key, value in profile.items():
                if key != 'positions':
                    flat_record[f'profile_{key}'] = value
            
            # 평탄화된 position 데이터 추가
            flat_record.update(position_data)
        
        # record의 다른 최상위 필드들 복사
        for key, value in record.items():
            if key != 'profile':
                flat_record[key] = value
                
        flattened_data.append(flat_record)
    
    return pd.DataFrame(flattened_data)

def converter(path:str ) -> int:
	df = OpenJson(path)
	excel_filename = path[:-4] + "xlsx"
	with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
		df.to_excel(writer, index=False, sheet_name='Data')
		
		# 열 너비 자동 조정
		worksheet = writer.sheets['Data']
		for idx, col in enumerate(df.columns):
			max_length = max(
				df[col].astype(str).str.len().max(),  # 데이터의 최대 길이
				len(str(col))  # 컬럼명의 길이
			)
			worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)  # 최대 50으로 제한
	
		return 0

if __name__=="__main__":
	if (len(sys.argv) != 2):
		print("Usage: Usage:script.py <JsonPath>")
		exit(1)
	else:
		PATH = sys.argv[1] if len(sys.argv) > 1 else None
	main()
