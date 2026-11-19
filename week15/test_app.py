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

r = client.get("/")
body = r.get_data(as_text=True)
tests.append((1, (r.status_code, "지역을 선택해주세요" in body), (200, True)))

app.ask_gemma = fake_good
body = client.get("/", query_string=WANDO).get_data(as_text=True)
tests.append((2, ("거점 도서관 없음" in body, "완도군에는 도서관이 3곳 있습니다." in body, "AI 요약" in body), (True, True, True)))

app.ask_gemma = fake_bad
body = client.get("/", query_string=WANDO).get_data(as_text=True)
tests.append((3, (FALLBACK in body, "기본 요약" in body, "99곳" in body), (True, True, False)))

app.ask_gemma = fake_error
r = client.get("/", query_string=WANDO)
body = r.get_data(as_text=True)
tests.append((4, (r.status_code, FALLBACK in body, "기본 요약" in body), (200, True, True)))

app.ask_gemma = fake_good
body = client.get("/", query_string={"region": "경상남도|완도군"}).get_data(as_text=True)
tests.append((5, ("등록된 도서관 정보가 없습니다" in body, "AI 요약" in body), (True, False)))

r = client.get("/smoking")
body = r.get_data(as_text=True)
tests.append((6, (r.status_code, "세종특별자치시" in body, "이용 기록 없음" in body), (200, True, True)))

tests.append((7, 0 <= body.find("세종특별자치시") < body.find("경상남도") < body.find("울산광역시"), True))

passed = 0
for num, actual, expected in tests:
    if actual == expected:
        passed += 1
    else:
        print(f"실패 {num}: 기대값 {expected}, 실제값 {actual}")
print(f"통과 {passed} / 전체 {len(tests)}")