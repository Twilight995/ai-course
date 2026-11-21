| 단계 | 한 일 | 테스트 명령 | 결과 | 날짜 |
| :--- | :--- | :--- | :--- | :--- |
| 1단계 | test_logic.py 및 logic.py 구현 | python test_logic.py | 통과 20 / 전체 20 | 2026. 11. 19. |
| 2단계 | load_smoking, smoking_priority 구현. 처음 통과 20 / 전체 28 → level_text 복구와 24~28번 비교 방식 수정 후 통과 | python test_logic.py | 통과 28 / 전체 28 | 2026. 11. 19. |
| 3단계 | fallback_summary, build_summary_prompt, is_safe_summary 구현 | python test_logic.py | 통과 41 / 전체 41 | 2026. 11. 19. |
| 4단계 | test_app.py, app.py, templates/index.html, templates/smoking.html 구현. 처음 통과 2 / 전체 7 → index.html의 깨진 select 부분 수정 후 통과 | python test_app.py | 통과 7 / 전체 7 | 2026. 11. 19. |
 | 5단계 | 스마트폰 최종 확인 | 아이폰 브라우저 직접 확인 | 확인표 5 / 5 통과 | 2026. 11. 19. |
| 준비 | data/welfare_gap.csv 추가, SPEC.md 를 v2 로 고침(이전 명세는 SPEC_v1.md), .clinerules 에 주소 이동 예외 추가 | python test_logic.py, python test_app.py | 통과 41 / 전체 41, 통과 7 / 전체 7 | 2026. 11. 21. |
 
 ## 5단계 스마트폰 확인표
 
 | 번호 | 확인한 것 | 결과 |
 | :--- | :--- | :--- |
 | 1 | 첫 화면에 "지역을 선택해주세요"가 보이고 글자가 확대 없이 읽힌다 | 통과 |
 | 2 | 전남광주통합특별시 완도군 → 빨강 카드, "거점 도서관 없음", 전체 3곳 | 통과 |
 | 3 | 경상남도 하동군 → 주황 카드, 전체 12곳, 주말 휴관 91.7% | 통과 |
 | 4 | 요약문에 "AI 요약" 표시가 보이고 카드에 없는 숫자가 없다 | 통과 |
 | 5 | 금연 지원 표 1위 세종특별자치시 "이용 기록 없음", 17위 울산광역시, 표가 화면을 넘지 않는다 | 통과 |

