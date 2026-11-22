import logic
from urllib.parse import quote

def run_tests():
    rows = logic.load_library()
    passed = 0
    total = 20

    # Test Cases
    tests = []

    # 1. len(load_library())
    tests.append((1, len(rows), 229))

    # 2. len(get_sido_list(rows))
    tests.append((2, len(logic.get_sido_list(rows)), 16))

    # 3. get_sido_list(rows)[0]
    tests.append((3, logic.get_sido_list(rows)[0], "강원특별자치도"))

    # 4. get_sigungu_list(rows, "제주특별자치도")
    tests.append((4, logic.get_sigungu_list(rows, "제주특별자치도"), ["서귀포시", "제주시"]))

    # 5. get_sigungu_list(rows, "없는도")
    tests.append((5, logic.get_sigungu_list(rows, "없는도"), []))

    # 6. gap_level(0, 66.7)
    tests.append((6, logic.gap_level(0, 66.7), "red"))

    # 7. gap_level(1, 50.0)
    tests.append((7, logic.gap_level(1, 50.0), "orange"))

    # 8. gap_level(1, 46.7)
    tests.append((8, logic.gap_level(1, 46.7), "green"))

    # 9. gap_level(4, 80.0)
    tests.append((9, logic.gap_level(4, 80.0), "green"))

    # 10. library_card(rows, "전남광주통합특별시", "완도군")
    card10, err10 = logic.library_card(rows, "전남광주통합특별시", "완도군")
    if err10 is None and card10 is not None:
        valid10 = (card10['total'] == 3 and card10['hub'] == 0 and card10['suspect'] == 3 and 
                   card10['weekend_closed'] == 2 and abs(card10['weekend_closed_pct'] - 66.7) < 0.1 and 
                   card10['level'] == "red" and card10['level_text'] == "거점 도서관 없음")
        tests.append((10, valid10, True))
    else:
        tests.append((10, (card10, err10), ({"total": 3, "hub": 0, "suspect": 3, "weekend_closed": 2, "weekend_closed_pct": 66.7, "level": "red", "level_text": "거점 도서관 없음"}, None)))

    # 11. library_card(rows, "경상남도", "하동군")
    card11, err11 = logic.library_card(rows, "경상남도", "하동군")
    if err11 is None and card11 is not None:
        valid11 = (card11['total'] == 12 and card11['hub'] == 1 and card11['small'] == 11 and 
                   abs(card11['weekend_closed_pct'] - 91.7) < 0.1 and card11['level'] == "orange" and 
                   card11['level_text'] == "거점 1곳 · 주말 휴관 많음")
        tests.append((11, valid11, True))
    else:
        tests.append((11, (card11, err11), ({"total": 12, "hub": 1, "small": 11, "weekend_closed_pct": 91.7, "level": "orange", "level_text": "거점 1곳 · 주말 휴관 많음"}, None)))

    # 12. library_card(rows, "강원특별자치도", "강릉시")
    card12, err12 = logic.library_card(rows, "강원특별자치도", "강릉시")
    if err12 is None and card12 is not None:
        valid12 = (card12['total'] == 11 and card12['hub'] == 4 and card12['level'] == "green" and card12['level_text'] == "균형")
        tests.append((12, valid12, True))
    else:
        tests.append((12, (card12, err12), ({"total": 11, "hub": 4, "level": "green", "level_text": "균형"}, None)))

    # 13. library_card(rows, "서울특별시", "중구")
    card13, err13 = logic.library_card(rows, "서울특별시", "중구")
    tests.append((13, card13['total'] if card13 else None, 19))

    # 14. library_card(rows, "부산광역시", "중구")
    card14, err14 = logic.library_card(rows, "부산광역시", "중구")
    tests.append((14, card14['total'] if card14 else None, 5))

    # 15. library_card(rows, "", "완도군")
    tests.append((15, logic.library_card(rows, "", "완도군"), (None, "시도를 선택해주세요")))

    # 16. library_card(rows, "경상남도", "  ")
    tests.append((16, logic.library_card(rows, "경상남도", "  "), (None, "시군구를 선택해주세요")))

    # 17. library_card(rows, None, None)
    tests.append((17, logic.library_card(rows, None, None), (None, "시도를 선택해주세요")))

    # 18. library_card(rows, "경상남도", "완도군")
    tests.append((18, logic.library_card(rows, "경상남도", "완도군"), (None, "등록된 도서관 정보가 없습니다")))

    # 19. library_card(rows, " 경상남도 ", " 하동군 ")
    card19, err19 = logic.library_card(rows, " 경상남도 ", " 하동군 ")
    if err19 is None and card19 is not None:
        tests.append((19, card19['total'], 12))
    else:
        tests.append((19, (card19, err19), ({"total": 12}, None)))

    # 20. 10번을 부른 뒤 "level" in rows[0]
    # Since we don't want to modify original rows, we check if the first row of the *original* rows has 'level'
    # However, the test says: 10번을 부른 뒤 "level" in rows[0]
    # We should ensure our library_card doesn't mutate original rows.
    # Let's check the original rows.
    tests.append((20, "level" in rows[0], False))

    # 21. len(load_smoking())
    srows = logic.load_smoking()
    tests.append((21, len(srows), 17))

    # 22. load_smoking()[0]
    tests.append((22, srows[0], {"region": "대구광역시", "registered": 12023, "high_pct": 21.8, "camp_use": 325, "camp_per_1000": 124.0}))

    # 23. len(result)
    result = logic.smoking_priority(srows)
    tests.append((23, len(result), 17))

    tests.append((24, (result[0]["region"], result[0]["rank"], result[0]["camp_use"]), ("세종특별자치시", 1, 0)))
    tests.append((25, (result[1]["region"], result[1]["rank"], result[1]["camp_per_1000"]), ("경상남도", 2, 108.0)))
    tests.append((26, (result[2]["region"], result[2]["rank"]), ("서울특별시", 3)))
    tests.append((27, (result[16]["region"], result[16]["rank"], result[16]["camp_per_1000"]), ("울산광역시", 17, 511.0)))
    tests.append((28, ("rank" in srows[0], srows[0]["region"]), (False, "대구광역시")))

    scard, serr = logic.library_card(rows, "전남광주통합특별시", "완도군")
    hcard, herr = logic.library_card(rows, "경상남도", "하동군")
    sprompt = logic.build_summary_prompt(scard)
    tests.append((29, logic.fallback_summary(scard), "전남광주통합특별시 완도군에는 등록된 도서관이 3곳 있고, 그중 대형 거점은 0곳입니다. 주말에 쉬는 곳은 66.7%입니다."))
    tests.append((30, logic.fallback_summary(hcard), "경상남도 하동군에는 등록된 도서관이 12곳 있고, 그중 대형 거점은 1곳입니다. 주말에 쉬는 곳은 91.7%입니다."))
    tests.append((31, "완도군" in sprompt, True))
    tests.append((32, "아래 숫자만 사용" in sprompt, True))
    tests.append((33, "두 문장" in sprompt, True))
    tests.append((34, "66.7" in sprompt, True))
    tests.append((35, "거점 도서관 없음" in sprompt, True))
    tests.append((36, logic.is_safe_summary(logic.fallback_summary(scard), scard), True))
    tests.append((37, logic.is_safe_summary("", scard), False))
    tests.append((38, logic.is_safe_summary(None, scard), False))
    tests.append((39, logic.is_safe_summary("완도군에는 도서관이 5곳 있습니다.", scard), False))
    tests.append((40, logic.is_safe_summary("완도군은 거점 도서관이 없습니다.", scard), True))
    tests.append((41, logic.is_safe_summary(logic.fallback_summary(hcard), hcard), True))
    gap = logic.load_gap()
    sinan = [r for r in gap if r["sigungu"] == "신안군"][0]
    yeongjong = [r for r in gap if r["sigungu"] == "영종구"][0]
    tests.append((42, len(gap), 230))
    tests.append((43, len(logic.get_sido_list(gap)), 16))
    tests.append((44, logic.get_sigungu_list(gap, "세종특별자치시"), ["세종시"]))
    tests.append((45, (sinan["pop"], type(sinan["pop"]).__name__, sinan["map_x"], sinan["lacking_count"]), (42337, "int", 60, 5)))
    tests.append((46, (sinan["access_pct"], sinan["doctors_per_1k"], type(sinan["doctors_per_1k"]).__name__), (85.5, 0.661, "float")))
    tests.append((47, (sinan["level_access"], sinan["cluster_name"], sinan["library_region"]), ("부족", "농어촌형", "전남광주통합특별시|신안군")))
    tests.append((48, (yeongjong["library_region"], yeongjong["new_gu"], yeongjong["access_source"]), ("", 1, "직선거리(2026)")))
    tests.append((49, logic.show_number(0), "0"))
    tests.append((50, logic.show_number(0.0), "0"))
    tests.append((51, logic.show_number(0.661), "0.66"))
    tests.append((52, logic.show_number(1.254), "1.3"))
    tests.append((53, logic.show_number(85.5), "85.5"))
    tests.append((54, logic.show_number(42.31), "42.3"))
    med = logic.gap_medians(gap)
    tests.append((55, len(logic.GAP_DOMAINS), 7))
    tests.append((56, [d["name"] for d in logic.GAP_DOMAINS], ["의료거리", "의료자원", "노인돌봄", "영유아보육", "아동돌봄", "장애인·복지", "도서관"]))
    tests.append((57, sum(len(d["items"]) for d in logic.GAP_DOMAINS), 17))
    tests.append((58, len(med), 17))
    tests.append((59, logic.show_number(med["doctors_per_1k"]), "1.3"))
    tests.append((60, logic.show_number(med["pharmacy_per_10k"]), "4.7"))
    tests.append((61, logic.show_number(med["senior_center_per_old_10k"]), "0.41"))
    tests.append((62, logic.show_number(med["lib_per_100k"]), "3.1"))
    tests.append((63, logic.gap_card(gap, "", ""), (None, "시도를 선택해주세요")))
    tests.append((64, logic.gap_card(gap, "인천광역시", ""), (None, "시군구를 선택해주세요")))
    tests.append((65, logic.gap_card(gap, "경상남도", "신안군"), (None, "등록된 지역 정보가 없습니다")))
    gcard, gmsg = logic.gap_card(gap, "전남광주통합특별시", "신안군")
    tests.append((66, (gmsg, gcard["pop"], gcard["lacking_count"], gcard["unsure_count"]), (None, 42337, 5, 1)))
    tests.append((67, [d["name"] for d in gcard["domains"]], ["의료거리", "의료자원", "노인돌봄", "영유아보육", "아동돌봄", "장애인·복지", "도서관"]))
    tests.append((68, [d["level"] for d in gcard["domains"]], ["부족", "경계", "부족", "부족", "비슷", "부족", "부족"]))
    tests.append((69, gcard["lacking_names"], ["의료거리", "노인돌봄", "영유아보육", "장애인·복지", "도서관"]))
    tests.append((70, gcard["domains"][1]["items"][0], {"label": "주민 천 명당 의사 수", "value": "0.66", "unit": "명", "median": "1.3", "raw": 0.661}))
    tests.append((71, (gcard["domains"][0]["lines"], gcard["domains"][1]["lines"]), (["이 지역 안에는 분만 가능한 기관이 없습니다."], ["기준선 가까이 있어 판정을 붙이지 않았습니다."])))
    tests.append((72, (gcard["domains"][0]["basis"] == logic.BASIS_ACCESS, gcard["domains"][2]["basis"] == logic.BASIS_NATION), (True, True)))
    tests.append((73, (gcard["cluster_name"], gcard["cluster_unsure"], gcard["library_region"]), ("농어촌형", 1, "전남광주통합특별시|신안군")))
    ycard, ymsg = logic.gap_card(gap, "인천광역시", "영종구")
    tests.append((74, (ycard["domains"][0]["level"], ycard["domains"][0]["basis"] == logic.BASIS_ACCESS_NEW), ("경계", True)))
    tests.append((75, ycard["domains"][0]["lines"], ["기준선 가까이 있어 판정을 붙이지 않았습니다.", "이 지역 안에는 지정 응급의료기관이 없습니다."]))
    tests.append((76, logic.gap_card(gap, "부산광역시", "중구")[0]["sido"], "부산광역시"))

    def notices(sido, sigungu):
        return logic.gap_notices(gap, logic.gap_card(gap, sido, sigungu)[0])
    tests.append((77, notices("전남광주통합특별시", "신안군"), []))
    tests.append((78, notices("서울특별시", "강남구"), []))
    tests.append((79, notices("경상북도", "울릉군"), ["주민이 3만 명보다 적어, 시설 한 곳 차이로 숫자가 크게 달라집니다."]))
    tests.append((80, notices("인천광역시", "제물포구"), ["2026년에 새로 생긴 구입니다. 어린이집·기초연금 등 일부 값은 옛 구의 값을 인구 비율로 나눈 추정입니다."]))
    tests.append((81, notices("인천광역시", "강화군"), ["장애인·복지 영역은 넉넉으로 나왔지만 '기초수급자 만 명당 사회복지관 수' 값은 0입니다. 다른 지표가 높아 넉넉이 된 것입니다."]))
    tests.append((82, notices("경상남도", "거창군"), ["의료거리는 차로 가는 시간 기준이라 넉넉으로 나왔습니다. 분만하려면 다른 지역으로 가야 합니다."]))
    tests.append((83, notices("부산광역시", "중구"), ["면적이 좁아 거리 값이 거칠게 계산됐습니다.", "의료거리는 차로 가는 시간 기준이라 넉넉으로 나왔습니다. 분만하려면 다른 지역으로 가야 합니다."]))
    top = logic.top_lacking(gap)
    tests.append((84, [(r["sigungu"], r["lacking_count"]) for r in top[:4]], [("미추홀구", 5), ("신안군", 5), ("용인시", 4), ("부평구", 4)]))
    tests.append((85, (len(top), top[9]["sigungu"]), (10, "금정구")))
    tests.append((86, len(logic.top_lacking(gap, 3)), 3))
    tests.append((87, top[0], {"sido": "인천광역시", "sigungu": "미추홀구", "lacking_count": 5, "unsure_count": 0, "pop": 419749}))
    tests.append((88, logic.sido_regions(gap, "세종특별자치시"), [{"sido": "세종특별자치시", "sigungu": "세종시", "lacking_count": 2, "unsure_count": 1, "pop": 390618}]))
    incheon = logic.sido_regions(gap, "인천광역시")
    tests.append((89, (len(incheon), [r["sigungu"] for r in incheon[:3]]), (11, ["미추홀구", "검단구", "부평구"])))
    tests.append((90, logic.sido_regions(gap, "없는도"), []))
    tests.append((91, [logic.dot_color(n) for n in range(6)], ["#7f9fc5", "#7f9fc5", "#e67e22", "#e67e22", "#c0392b", "#c0392b"]))
    nat = logic.map_points(gap)
    tests.append((92, (nat["width"], nat["height"], len(nat["points"])), (1000, 1240, 230)))
    tests.append((93, nat["points"][0], {"x": 268, "y": 466, "color": "#7f9fc5", "sido": "충청남도", "sigungu": "공주시", "lacking_count": 0}))
    tests.append((94, nat["points"][-1], {"x": 60, "y": 853, "color": "#c0392b", "sido": "전남광주통합특별시", "sigungu": "신안군", "lacking_count": 5}))
    seoul = logic.map_points(gap, "서울특별시")
    tests.append((95, (seoul["width"], seoul["height"], len(seoul["points"])), (1000, 826, 25)))
    tests.append((96, (seoul["points"][0], seoul["points"][-1]), ({"x": 97, "y": 524, "color": "#7f9fc5", "sido": "서울특별시", "sigungu": "양천구", "lacking_count": 0}, {"x": 334, "y": 713, "color": "#c0392b", "sido": "서울특별시", "sigungu": "관악구", "lacking_count": 4})))
    tests.append((97, logic.map_points(gap, "세종특별자치시"), {"width": 1000, "height": 300, "points": [{"x": 500, "y": 150, "color": "#e67e22", "sido": "세종특별자치시", "sigungu": "세종시", "lacking_count": 2}]}))
    incheon_map = logic.map_points(gap, "인천광역시")
    tests.append((98, (incheon_map["height"], incheon_map["points"][-1]["sigungu"], incheon_map["points"][-1]["x"], incheon_map["points"][-1]["y"]), (478, "미추홀구", 889, 367)))
    tests.append((99, logic.map_points(gap, "없는도"), {"width": 1000, "height": 300, "points": []}))
    nat_svg = logic.build_map_svg(nat)
    tests.append((100, (nat_svg.startswith('<svg viewBox="0 0 1000 1240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="점 지도">'), nat_svg.endswith("</svg>")), (True, True)))
    tests.append((101, (nat_svg.count("<circle"), nat_svg.count("<a href="), nat_svg.count("<text")), (230, 230, 0)))
    tests.append((102, '<a href="/region?region=' + quote("전남광주통합특별시|신안군") + '">' in nat_svg, True))
    tests.append((103, '<circle cx="60" cy="853" r="9" fill="#c0392b"><title>전남광주통합특별시 신안군 · 부족 5개</title></circle>' in nat_svg, True))
    seoul_svg = logic.build_map_svg(seoul, True)
    tests.append((104, (seoul_svg.startswith('<svg viewBox="0 0 1000 826"'), seoul_svg.count("<circle"), seoul_svg.count("<text")), (True, 25, 25)))
    tests.append((105, '<circle cx="334" cy="713" r="22" fill="#c0392b"><title>서울특별시 관악구 · 부족 4개</title></circle>' in seoul_svg, True))
    tests.append((106, '<text x="362" y="723" font-size="30">관악구</text>' in seoul_svg, True))
    empty_svg = logic.build_map_svg(logic.map_points(gap, "없는도"), True)
    tests.append((107, (empty_svg.startswith('<svg viewBox="0 0 1000 300"'), empty_svg.endswith("</svg>"), empty_svg.count("<circle")), (True, True, 0)))
    jcard = logic.gap_card(gap, "인천광역시", "제물포구")[0]
    tests.append((108, logic.gap_fallback_summary(gcard), "신안군의 7개 영역 가운데 5개가 부족으로 나왔습니다. 부족한 영역은 의료거리, 노인돌봄, 영유아보육, 장애인·복지, 도서관입니다."))
    tests.append((109, logic.gap_fallback_summary(jcard), "제물포구의 7개 영역 가운데 부족으로 나온 영역은 없습니다."))
    tests.append((110, len(logic.gap_fallback_summary(gcard)) <= 200, True))
    tests.append((111, "7" in logic.gap_fallback_summary(jcard), True))
    tests.append((112, logic.is_safe_gap_summary(logic.gap_fallback_summary(gcard), gcard), True))
    tests.append((113, logic.is_safe_gap_summary(logic.gap_fallback_summary(jcard), jcard), True))
    tests.append((114, logic.is_safe_gap_summary("신안군은 7개 영역 가운데 5개가 부족합니다. 제때 가기 어려운 주민이 85.5%입니다.", gcard), True))
    tests.append((115, logic.is_safe_gap_summary("신안군은 7개 영역 가운데 5개가 부족합니다. 제때 가기 어려운 주민이 99%입니다.", gcard), False))
    tests.append((116, (logic.is_safe_gap_summary("재가노인복지시설이 0.84곳입니다.", gcard), logic.is_safe_gap_summary("재가노인복지시설이 0.841곳입니다.", gcard)), (True, False)))
    tests.append((117, (logic.is_safe_gap_summary("신안군은 아동돌봄이 부족합니다.", gcard), logic.is_safe_gap_summary("제물포구는 도서관이 부족합니다.", jcard)), (False, False)))
    tests.append((118, (logic.is_safe_gap_summary(None, gcard), logic.is_safe_gap_summary("  ", gcard)), (False, False)))
    tests.append((119, logic.is_safe_gap_summary("가" * 201, gcard), False))

    gprompt = logic.build_gap_prompt(gcard)
    tests.append((120, ("전남광주통합특별시 신안군" in gprompt, "- 부족한 영역 수: 5" in gprompt), (True, True)))
    tests.append((121, "- 부족한 영역: 의료거리, 노인돌봄, 영유아보육, 장애인·복지, 도서관" in gprompt, True))
    tests.append((122, "- [의료거리] 응급실·분만실·소아청소년과에 제때 가기 어려운 주민 비율: 85.5%" in gprompt, True))
    tests.append((123, "- [노인돌봄] 노인 만 명당 노인복지관 수: 0곳" in gprompt, True))
    tests.append((124, ("의료자원" in gprompt, "아동돌봄" in gprompt), (False, False)))
    tests.append((125, ("부족으로 나온 영역이 없다" in logic.build_gap_prompt(jcard), "[" in logic.build_gap_prompt(jcard)), (True, False)))

    for num, actual, expected in tests:
        if actual == expected:
            passed += 1
        else:
            print(f"실패 {num}: 기대값 {expected}, 실제값 {actual}")

    total = len(tests)
    print(f"통과 {passed} / 전체 {total}")

if __name__ == "__main__":
    run_tests()