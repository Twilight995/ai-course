import app
import logic
import build_site
import os
import tempfile
import csv
import build_site
import fetch_summaries
import json
import make_site

tests = []
rows = logic.load_gap()
card, _ = logic.gap_card(rows, "전남광주통합특별시", "신안군")
GOOD = "신안군은 7개 영역 가운데 5개가 부족합니다. 제때 가기 어려운 주민이 85.5%입니다."
FALLBACK = "신안군의 7개 영역 가운데 5개가 부족으로 나왔습니다. 부족한 영역은 의료거리, 노인돌봄, 영유아보육, 장애인·복지, 도서관입니다."

calls = []
def fake_good(prompt):
    calls.append(prompt)
    return GOOD
def fake_bad(prompt):
    calls.append(prompt)
    return "신안군에는 병원이 99곳 있습니다."
def fake_error(prompt):
    calls.append(prompt)
    raise RuntimeError("연결 실패")
def fake_second(prompt):
    calls.append(prompt)
    return GOOD if len(calls) == 2 else "잘 모르겠습니다."

app.ask_gemma = fake_good
tests.append((1, (fetch_summaries.fetch_one(card), len(calls)), ((GOOD, "AI 요약 (미리 받아 둔 글)"), 1)))
calls.clear()
app.ask_gemma = fake_bad
tests.append((2, (fetch_summaries.fetch_one(card), len(calls)), ((FALLBACK, "기본 요약"), 3)))
calls.clear()
app.ask_gemma = fake_error
tests.append((3, (fetch_summaries.fetch_one(card), len(calls)), ((FALLBACK, "기본 요약"), 3)))
calls.clear()
app.ask_gemma = fake_second
tests.append((4, (fetch_summaries.fetch_one(card), len(calls)), ((GOOD, "AI 요약 (미리 받아 둔 글)"), 2)))
calls.clear()
app.ask_gemma = fake_bad
tests.append((5, (fetch_summaries.fetch_one(card, 1), len(calls)), ((FALLBACK, "기본 요약"), 1)))
tests.append((6, build_site.cut_container('<body><div class="container"> <h1>가</h1><div>나</div> </div></body>'), '<h1>가</h1><div>나</div>'))
tests.append((7, build_site.fix_links('<a href="/region?region=A%7CB">x</a><a href="/?sido=S">y</a><a href="/">z</a><form action="/">'), '<a href="#region=A%7CB">x</a><a href="#sido=S">y</a><a href="#">z</a><form action="/">'))
tests.append((8, build_site.load_summaries("없는파일.csv"), {}))
tmp = os.path.join(tempfile.gettempdir(), "gap_summaries_test.csv")
with open(tmp, mode="w", encoding="utf-8-sig", newline="") as f:
    csv.writer(f).writerows([["sido", "sigungu", "summary", "label"], ["서울특별시", "관악구", "첫 문장, 쉼표 있음.", "기본 요약"]])
tests.append((9, build_site.load_summaries(tmp), {"서울특별시|관악구": ("첫 문장, 쉼표 있음.", "기본 요약")}))
os.remove(tmp)
saved = build_site.load_summaries()
tests.append((10, (len(saved), set(label for text, label in saved.values()) <= {"AI 요약 (미리 받아 둔 글)", "기본 요약"}, "서울특별시|관악구" in saved), (230, True, True)))
gwanak, _ = logic.gap_card(rows, "서울특별시", "관악구")
yangcheon, _ = logic.gap_card(rows, "서울특별시", "양천구")
tests.append((11, build_site.replace_block('<p>a</p><div class="x"><b>1</b></div><p>z</p>', '<div class="x">', '<i></i>'), '<p>a</p><i></i><p>z</p>'))
tests.append((12, build_site.replace_block('<p>a</p>', '<div class="x">', '<i></i>'), '<p>a</p>'))
info = build_site.summary_info(gwanak, ("글", "기본 요약"))
tests.append((13, (info["allowed"], info["banned"], info["count"]), (["0.10", "0.34", "1.0", "1.1", "1.4", "1.9", "4", "4.8", "5.1", "5.7", "7", "7.4", "7.5"], ["의료거리", "영유아보육", "아동돌봄"], 4)))
tests.append((14, (info["saved"], info["saved_label"], info["prompt"] == logic.build_gap_prompt(gwanak), sorted(info.keys())), ("글", "기본 요약", True, ["allowed", "banned", "count", "prompt", "saved", "saved_label"])))
info = build_site.summary_info(yangcheon, ("가", "나"))
tests.append((15, (info["allowed"], len(info["banned"]), info["count"]), (["0", "7"], 7, 0)))
app.ask_gemma = fake_error
calls.clear()
site = make_site.build_all(saved)
tests.append((16, (len(site["home"]), len(site["regions"]), len(site["colors"]), len(site["summary"]), len(site["legends"]), len(calls)), (17, 230, 230, 230, 8, 0)))
pieces = "".join(site["home"].values()) + "".join(site["regions"].values()) + site["missing"]
tests.append((17, (pieces.count('href="/'), pieces.count("도서관 자세히"), pieces.count('<div class="panel summary" id="summary"><strong></strong><p></p></div>'), pieces.count('class="panel summary"')), (0, 0, 230, 230)))
tests.append((18, (site["home"][""].count("<path"), site["home"]["서울특별시"].count("<path"), site["home"]["서울특별시"].startswith("<h1>서울특별시</h1>"), 'href="#region=' in site["home"][""]), (230, 25, True, True)))
tests.append((19, site["colors"]["서울특별시|관악구"], {"": "#c0392b", "access": "#2e7d5b", "medical": "#c0392b", "elder": "#c0392b", "infant": "#2e7d5b", "child": "#7a828c", "disabled": "#c0392b", "library": "#c0392b"}))
tests.append((20, (site["legends"]["access"]["note"], len(site["legends"][""]["legend"]), len(site["legends"]["access"]["legend"])), ("의료거리 영역의 판정으로 칠했습니다. 구역을 누르면 그 지역으로 갑니다.", 3, 4)))
tests.append((21, ("등록된 지역 정보가 없습니다" in site["missing"], 'href="#"' in site["missing"], site["regions"]["전남광주통합특별시|신안군"].count('class="chip"'), "7개 영역 중 5개 부족, 1개 경계" in site["regions"]["전남광주통합특별시|신안군"]), (True, True, 7, True)))
tests.append((22, (site["summary"]["전남광주통합특별시|신안군"]["saved"], site["summary"]["전남광주통합특별시|신안군"]["saved_label"]), saved["전남광주통합특별시|신안군"]))
tests.append((23, make_site.build_all({})["summary"]["전남광주통합특별시|신안군"]["saved"], FALLBACK))
out = os.path.join(tempfile.gettempdir(), "site_data_test.js")
make_site.main(out)
with open(out, encoding="utf-8") as f:
    written = f.read()
os.remove(out)
tests.append((24, (written.startswith("const SITE = {"), written.endswith("};"), sorted(json.loads(written[13:-1]).keys())), (True, True, ["colors", "home", "legends", "missing", "regions", "summary"])))

passed = 0
for num, actual, expected in tests:
    if actual == expected:
        passed += 1
    else:
        print(f"실패 {num}: 실제 {actual} / 기대 {expected}")
print(f"통과 {passed} / 전체 {len(tests)}")