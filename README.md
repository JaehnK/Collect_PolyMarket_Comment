# Polymarket 데이터 도구
###### Polymarket 댓글 수집 및 데이터 변환을 위한 Python 스크립트입니다.

### 기능
- Polymarket URL에서 이벤트 정보 추출 및 댓글 수집
- JSON 데이터 구조 시각화
- Excel/CSV 변환 및 자동 포맷팅
- 오류 처리 및 속도 제한

### 필수 패키지 설치
```
pip install requests pandas numpy openpyxl
```

### 사용법
```
python ./main.py <polymarket URL>

# 예시
python ./main.py https://polymarket.com/event/will-trump-create-a-national-bitcoin-reserve-in-his-first-100-days?tid=1737788511144
```

### 출력파일
- `polymarket_comments_<이벤트ID>_<댓글수>.json`: 수집된 댓글
- `[원본파일명].xlsx`: 변환된 Excel 파일

### 오류 처리
- 네트워크 오류 시 자동 저장
- JSON 파싱 오류 처리
- API 요청 제한 관리

### 요구사항
- Python 3.6+
- `requests`
- `pandas`
- `numpy`
- `openpyxl`

### 라이선스
###### MIT 라이선스