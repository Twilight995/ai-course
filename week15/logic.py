import csv

def load_library(path="data/library_gap.csv"):
    rows = []
    with open(path, mode='r', encoding='utf-8-sig') as f:
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
    # Check for empty or None sido/sigungu
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