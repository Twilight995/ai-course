import logic

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

    for num, actual, expected in tests:
        if actual == expected:
            passed += 1
        else:
            print(f"실패 {num}: 기대값 {expected}, 실제값 {actual}")

    total = len(tests)
    print(f"통과 {passed} / 전체 {total}")

if __name__ == "__main__":
    run_tests()