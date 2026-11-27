import app

client = app.app.test_client()
tests = []

def fake_good(prompt):
    return "완도군에는 도서관이 3곳 있습니다."

def fake_bad(prompt):
    return "완도군에는 도서관이 99곳 있습니다."

def fake_error(prompt):
    raise Exception("서버 오류")

WANDO = {"region": "전남광주통합특별시|완도군"}
FALLBACK = "전남광주통합특별시 완도군에는 등록된 도서관이 3곳 있고, 그중 대형 거점은 0곳입니다. 주말에 쉬는 곳은 66.7%입니다."

r = client.get("/library")
body = r.get_data(as_text=True)
tests.append((1, (r.status_code, "지역을 선택해주세요" in body), (200, True)))

app.ask_gemma = fake_good
body = client.get("/library", query_string=WANDO).get_data(as_text=True)
tests.append((2, ("거점 도서관 없음" in body, "완도군에는 도서관이 3곳 있습니다." in body, "AI 요약" in body), (True, True, True)))

app.ask_gemma = fake_bad
body = client.get("/library", query_string=WANDO).get_data(as_text=True)
tests.append((3, (FALLBACK in body, "기본 요약" in body, "99곳" in body), (True, True, False)))

app.ask_gemma = fake_error
r = client.get("/library", query_string=WANDO)
body = r.get_data(as_text=True)
tests.append((4, (r.status_code, FALLBACK in body, "기본 요약" in body), (200, True, True)))

app.ask_gemma = fake_good
body = client.get("/library", query_string={"region": "경상남도|완도군"}).get_data(as_text=True)
tests.append((5, ("등록된 도서관 정보가 없습니다" in body, "AI 요약" in body), (True, False)))

r = client.get("/smoking")
body = r.get_data(as_text=True)
tests.append((6, (r.status_code, "세종특별자치시" in body, "이용 기록 없음" in body), (200, True, True)))

tests.append((7, 0 <= body.find("세종특별자치시") < body.find("경상남도") < body.find("울산광역시"), True))
lib_body = client.get("/library").get_data(as_text=True)
smoke_body = client.get("/smoking").get_data(as_text=True)
tests.append((8, ("action=\"/library\"" in lib_body, "← 격차맵으로" in lib_body, "href=\"/\"" in lib_body), (True, True, True)))
tests.append((9, ("<nav" in lib_body, "<nav" in smoke_body), (False, False)))

r = client.get("/")
home_body = r.get_data(as_text=True)
tests.append((10, (r.status_code, "공공복지격차맵" in home_body, "지역을 선택해주세요" in home_body), (200, True, True)))
tests.append((11, (home_body.count("<path"), 'viewBox="0 0 1000 953"' in home_body), (230, True)))
tests.append((12, (home_body.count("<option"), 'name="sido"' in home_body, 'name="domain"' in home_body), (25, True, True)))
tests.append((13, ("인천광역시 미추홀구" in home_body, home_body.count('class="row"'), "부족 5개" in home_body), (True, 10, True)))
tests.append((14, ("부족 4개 이상" in home_body, "<nav" in home_body, "<script" in home_body), (True, False, False)))
seoul_body = client.get("/", query_string={"sido": "서울특별시"}).get_data(as_text=True)
tests.append((15, ('viewBox="300.0 169.0 60.5 50.8"' in seoul_body, seoul_body.count("<path"), "관악구</text>" in seoul_body), (True, 25, True)))
tests.append((16, (seoul_body.count('class="row"'), "경계" in seoul_body, "지역을 선택해주세요" in seoul_body), (25, False, False)))
none_body = client.get("/", query_string={"sido": "없는도"}).get_data(as_text=True)
tests.append((17, ("등록된 지역 정보가 없습니다" in none_body, none_body.count("<path")), (True, 230)))
GAP_GOOD = "신안군은 7개 영역 가운데 5개가 부족합니다. 제때 가기 어려운 주민이 85.5%입니다."
GAP_FALLBACK = "신안군의 7개 영역 가운데 5개가 부족으로 나왔습니다. 부족한 영역은 의료거리, 노인돌봄, 영유아보육, 장애인·복지, 도서관입니다."
SINAN = {"region": "전남광주통합특별시|신안군"}
app.ask_gemma = lambda prompt: GAP_GOOD
sinan_body = client.get("/region", query_string=SINAN).get_data(as_text=True)
tests.append((18, ("전남광주통합특별시 신안군" in sinan_body, "인구 42,337명" in sinan_body, "7개 영역 중 5개 부족</strong>" in sinan_body), (True, True, True)))
tests.append((19, (GAP_GOOD in sinan_body, "AI 요약" in sinan_body), (True, True)))
tests.append((20, (sinan_body.count('<div class="card"'), "의료거리 · 부족" in sinan_body, "의료자원 · 보통" in sinan_body), (7, True, True)))
tests.append((21, ("주민 천 명당 의사 수 0.66명 (전국 중앙값 1.3명)" in sinan_body, "이 지역 안에는 분만 가능한 기관이 없습니다." in sinan_body, "전국 230곳과 견준 판정" in sinan_body), (True, True, True)))
tests.append((22, ("유형: 농어촌형 (두 유형의 중간에 가까움)" in sinan_body, "알아 둘 점" in sinan_body, 'href="/library?region=' in sinan_body), (True, False, True)))
app.ask_gemma = lambda prompt: "신안군은 7개 영역 가운데 5개가 부족합니다. 제때 가기 어려운 주민이 99%입니다."
bad_body = client.get("/region", query_string=SINAN).get_data(as_text=True)
tests.append((23, (GAP_FALLBACK in bad_body, "기본 요약" in bad_body, "99%" in bad_body), (True, True, False)))
app.ask_gemma = fake_error
r = client.get("/region", query_string=SINAN)
tests.append((24, (r.status_code, GAP_FALLBACK in r.get_data(as_text=True)), (200, True)))
app.ask_gemma = lambda prompt: GAP_GOOD
ganghwa_body = client.get("/region", query_string={"region": "인천광역시|강화군"}).get_data(as_text=True)
tests.append((25, ("알아 둘 점" in ganghwa_body, "장애인·복지 영역은 넉넉으로 나왔지만" in ganghwa_body), (True, True)))
yeongjong_body = client.get("/region", query_string={"region": "인천광역시|영종구"}).get_data(as_text=True)
tests.append((26, ("/library" in yeongjong_body, "2026년에 새로 생긴 구입니다." in yeongjong_body), (False, True)))
tests.append((27, "지역을 선택해주세요" in client.get("/region").get_data(as_text=True), True))
tests.append((28, "시군구를 선택해주세요" in client.get("/region", query_string={"region": "인천광역시|"}).get_data(as_text=True), True))
wrong_body = client.get("/region", query_string={"region": "경상남도|신안군"}).get_data(as_text=True)
tests.append((29, ("등록된 지역 정보가 없습니다" in wrong_body, "AI 요약" in wrong_body, "<script" in sinan_body, "<nav" in sinan_body), (True, False, False, False)))
tests.append((30, "요약:" in sinan_body, False))
tests.append((31, ("background-color: #ffffff" in home_body, "background-color: #ffffff" in sinan_body), (True, True)))
app.ask_gemma = lambda prompt: "잘 모르겠습니다."
tests.append((32, "기본 요약" in client.get("/region", query_string=SINAN).get_data(as_text=True), True))
access_body = client.get("/", query_string={"domain": "access"}).get_data(as_text=True)
tests.append((33, (access_body.count('fill="#2e7d5b"'), "의료거리 영역의 판정으로 칠했습니다" in access_body, 'value="access" selected' in access_body), (161, True, True)))
tests.append((34, ("부족 4개 이상" in access_body, "넉넉</span>" in access_body, "보통</span>" in access_body, "비슷</span>" in access_body, "부족 → 보통 → 넉넉 순서입니다" in access_body), (False, True, True, False, True)))
tests.append((35, client.get("/static/style.css").status_code, 200))
tests.append((36, ['href="/static/style.css"' in b for b in (home_body, sinan_body, lib_body, smoke_body)], [True, True, True, True]))
tests.append((37, (sinan_body.count('class="chip"'), 'class="btn' in sinan_body, 'class="btn' in home_body), (7, True, True)))
tests.append((38, ('class="hint"' in sinan_body, 'class="alert"' in sinan_body, "경계" in sinan_body, "비슷</span>" in sinan_body, "기준선에 가까운 보통입니다" in sinan_body), (True, True, False, False, True)))

passed = 0
for num, actual, expected in tests:
    if actual == expected:
        passed += 1
    else:
        print(f"실패 {num}: 기대값 {expected}, 실제값 {actual}")
print(f"통과 {passed} / 전체 {len(tests)}")
