 # 우리 지역 공공데이터 요약
 
 스마트폰에서 보기 어려운 공공데이터 CSV를 지역별 카드와 표로 보여주는 모바일 웹
 
 ## 실행 방법
 pip install flask openai → python app.py → 같은 와이파이의 스마트폰에서 http://PC주소:5000
 
 ## 테스트 방법
 python test_logic.py (통과 41 / 전체 41), python test_app.py (통과 7 / 전체 7)
 
 ## 파일 설명
 - app.py: Flask 웹 서버
 - logic.py: 데이터 계산 및 처리 로직
 - templates/: HTML 템플릿 파일들
 - data/: 집계된 공공데이터 CSV 파일들
 - test_logic.py: 로직 검증 테스트
 - test_app.py: Flask 앱 검증 테스트
 - SPEC.md: 프로젝트 사양서
 - PROGRESS.md: 작업 진행 기록
 
 ## 스크린샷
 screenshots/ 폴더에 아이폰에서 찍은 화면 4장이 있다
 
 ## 자료 출처
 - 공공데이터포털 전국도서관표준데이터
 - 국가금연지원서비스 니코틴의존도(2024)
 
 ## 사용 모델
 - 실습 서버 gemma4 (Cline으로 개발, 요약문 생성에도 사용)