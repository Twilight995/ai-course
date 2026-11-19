import csv
import re

def load_library(path="data/library_gap.csv"):
    rows = []
    with open(path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_row = {
                "sido": row["시도"],
                "sigungu": row["시군구"],
                "total": int(row["전체"]),
                "hub": int(row["거점"]),
                "small": int(row["동네"]),
                "suspect": int(row["오류의심"]),
                "reading": int(row["열람전용"]),
                "weekend_closed": int(row["주말휴관"]),
                "weekend_closed_pct": float(row["주말휴관비율"])
            }
            rows.append(new_row)
    return rows

def get_sido_list(rows):
    sidos = set()
    for row in rows:
        sidos.add(row["sido"])
    return sorted(list(sidos))

def get_sigungu_list(rows, sido):
    sigungus = set()
    for row in rows:
        if row["sido"] == sido:
            sigungus.add(row["sigungu"])
    return sorted(list(sigungus))

def gap_level(hub, weekend_closed_pct):
    if hub == 0:
        return "red"
    elif hub == 1 and weekend_closed_pct >= 50:
        return "orange"
    else:
        return "green"

def library_card(rows, sido, sigungu):
    sido_clean = str(sido).strip() if sido is not None else ""
    sigungu_clean = str(sigungu).strip() if sigungu is not None else ""

    if not sido_clean:
        return (None, "시도를 선택해주세요")
    if not sigungu_clean:
        return (None, "시군구를 선택해주세요")

    for row in rows:
        if row["sido"].strip() == sido_clean and row["sigungu"].strip() == sigungu_clean:
            card = row.copy()
            level = gap_level(card["hub"], card["weekend_closed_pct"])
            card["level"] = level
            
            if level == "red":
                level_text = "거점 도서관 없음"
            elif level == "orange":
                level_text = "거점 1곳 · 주말 휴관 많음"
            else:
                level_text = "균형"

            card["level_text"] = level_text
            return (card, None)
            
    return (None, "등록된 도서관 정보가 없습니다")

def load_smoking(path="data/smoking_resource.csv"):
    rows = []
    with open(path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_row = {
                "region": row["지역"],
                "registered": int(row["등록자"]),
                "high_pct": float(row["고의존비율"]),
                "camp_use": int(row["캠프이용"]),
                "camp_per_1000": float(row["고의존1000명당캠프"])
            }
            rows.append(new_row)
    return rows

def smoking_priority(rows):
    sorted_rows = sorted(rows, key=lambda x: x["camp_per_1000"])
    result = []
    for i, row in enumerate(sorted_rows):
        new_row = dict(row)
        new_row["rank"] = i + 1
        result.append(new_row)
    return result

def fallback_summary(card):
    return f"{card['sido']} {card['sigungu']}에는 등록된 도서관이 {card['total']}곳 있고, 그중 대형 거점은 {card['hub']}곳입니다. 주말에 쉬는 곳은 {card['weekend_closed_pct']}%입니다."
def build_summary_prompt(card):
    return (f"아래 숫자만 사용해서 {card['sido']} {card['sigungu']}의 도서관 현황을 한국어 두 문장으로 설명해줘. "
            f"도서관을 세는 단위는 '곳'을 써야 해. 아래에 없는 숫자는 쓰지 마.\n"
            f"- 전체 도서관: {card['total']}곳\n"
            f"- 대형 거점 도서관: {card['hub']}곳\n"
            f"- 동네 도서관: {card['small']}곳\n"
            f"- 주말 휴관 비율: {card['weekend_closed_pct']}%\n"
            f"- 상태: {card['level_text']}")

def is_safe_summary(text, card):
    if text is None or not text.strip():
        return False
    
    allowed_numbers = {float(card['total']), float(card['hub']), float(card['small']), 
                       float(card['suspect']), float(card['reading']), 
                       float(card['weekend_closed']), float(card['weekend_closed_pct'])}
    
    numbers_in_text = re.findall(r"\d+(?:\.\d+)?", text)
    for num_str in numbers_in_text:
        if float(num_str) not in allowed_numbers:
            return False
    return True
