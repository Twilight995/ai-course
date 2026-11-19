| 단계 | 한 일 | 테스트 명령 | 결과 | 날짜 |
| :--- | :--- | :--- | :--- | :--- |
| 1단계 | test_logic.py 및 logic.py 구현 | python test_logic.py | 통과 20 / 전체 20 | 2026. 11. 19. |
| 2단계 | load_smoking, smoking_priority 구현. 처음 통과 20 / 전체 28 → level_text 복구와 24~28번 비교 방식 수정 후 통과 | python test_logic.py | 통과 28 / 전체 28 | 2026. 11. 19. |
| 3단계 | fallback_summary, build_summary_prompt, is_safe_summary 구현 | python test_logic.py | 통과 41 / 전체 41 | 2026. 11. 19. |
| 4단계 | test_app.py, app.py, templates/index.html, templates/smoking.html 구현. 처음 통과 2 / 전체 7 → index.html의 깨진 select 부분 수정 후 통과 | python test_app.py | 통과 7 / 전체 7 | 2026. 11. 19. |
