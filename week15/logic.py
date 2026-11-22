import csv
import re
import statistics
from urllib.parse import quote

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


def build_gap_prompt(card):
    if card["lacking_count"] == 0:
        return f"{card['sido']} {card['sigungu']}의 공공복지 상황을 한국어 한 문장으로 말해줘.\n7개 영역 가운데 부족으로 나온 영역이 없다고 말해. 숫자는 7만 쓰고, 영역 이름은 쓰지 마."

    lines = [
        f"아래 정보만 써서 {card['sido']} {card['sigungu']}의 공공복지 상황을 한국어 두 문장으로 설명해줘.",
        "첫 문장에는 7개 영역 가운데 몇 개가 부족으로 나왔는지와 부족한 영역의 이름을 말해.",
        "둘째 문장에는 아래 지표 가운데 하나를 골라 그 숫자를 그대로 말해.",
        "아래에 없는 숫자와 아래에 없는 영역 이름은 쓰지 마. 숫자를 바꾸거나 계산하지 마.",
        f"- 부족한 영역 수: {card['lacking_count']}",
        f"- 부족한 영역: {', '.join(card['lacking_names'])}"
    ]

    for domain in card.get("domains", []):
        if domain.get("level") == "부족":
            for item in domain.get("items", []):
                lines.append(f"- [{domain['name']}] {item['label']}: {item['value']}{item['unit']}")

    return "\n".join(lines)
def gap_card(rows, sido, sigungu):
    if not sido:
        return (None, "시도를 선택해주세요")
    if not sigungu:
        return (None, "시군구를 선택해주세요")
    
    row = None
    for r in rows:
        if r["sido"] == sido and r["sigungu"] == sigungu:
            row = r
            break
    
    if row is None:
        return (None, "등록된 지역 정보가 없습니다")
    
    medians = gap_medians(rows)
    domains_list = []
    lacking_names = []
    
    for domain in GAP_DOMAINS:
        key = domain["key"]
        name = domain["name"]
        level = row["level_" + key]
        
        basis = domain["basis"]
        if key == "access" and row.get("access_source") == "직선거리(2026)":
            basis = BASIS_ACCESS_NEW
            
        items = []
        for item_info in domain["items"]:
            item_key, label, unit = item_info
            val = row[item_key]
            items.append({
                "label": label,
                "value": show_number(val),
                "unit": unit,
                "median": show_number(medians[item_key]),
                "raw": val
            })
            
        lines = []
        if level == "경계":
            lines.append("기준선 가까이 있어 판정을 붙이지 않았습니다.")
        if key == "access" and row.get("no_delivery_room") == 1:
            lines.append("이 지역 안에는 분만 가능한 기관이 없습니다.")
        if key == "access" and row.get("no_er") == 1:
            lines.append("이 지역 안에는 지정 응급의료기관이 없습니다.")
            
        domains_list.append({
            "key": key,
            "name": name,
            "level": level,
            "basis": basis,
            "items": items,
            "lines": lines
        })
        
        if level == "부족":
            lacking_names.append(name)
            
    card = {
        "sido": row["sido"],
        "sigungu": row["sigungu"],
        "pop": row["pop"],
        "lacking_count": row["lacking_count"],
        "unsure_count": row["unsure_count"],
        "cluster_name": row["cluster_name"],
        "cluster_unsure": row["cluster_unsure"],
        "library_region": row["library_region"],
        "domains": domains_list,
        "lacking_names": lacking_names
    }
    
    return (card, None)

BASIS_ACCESS = "정부 기준(응급실 30분·분만실 60분·소아청소년과 60분 안에 못 가는 주민 비율 중 가장 큰 값). 50% 이상이면 부족, 10% 미만이면 넉넉"
BASIS_ACCESS_NEW = "새로 생긴 구라 정부 값이 없어, 직접 잰 직선거리 기준(응급 10km·분만 20km·소아청소년과 10km 밖 주민 비율)으로 대신함. 잣대가 달라 기준선(50%, 10%) 가까이 있으면 판정을 붙이지 않음"
BASIS_PEER = "인구 구조가 비슷한 지역과 견준 판정"
BASIS_NATION = "전국 230곳과 견준 판정"

# 영역 7개. items 는 (자료의 칸 이름, 화면에 쓸 이름표, 단위) 이다. 이름표에는 숫자를 쓰지 않는다.
GAP_DOMAINS = [
    {"key": "access", "name": "의료거리", "basis": BASIS_ACCESS, "items": [
        ("access_pct", "응급실·분만실·소아청소년과에 제때 가기 어려운 주민 비율", "%"),
    ]},
    {"key": "medical", "name": "의료자원", "basis": BASIS_PEER, "items": [
        ("doctors_per_1k", "주민 천 명당 의사 수", "명"),
        ("clinic_per_10k", "주민 만 명당 의원 수", "곳"),
        ("pharmacy_per_10k", "주민 만 명당 약국 수", "곳"),
        ("pediatric_per_child_10k", "아동 만 명당 소아청소년과 수", "곳"),
        ("obgyn_per_100k", "주민 십만 명당 산부인과 수", "곳"),
    ]},
    {"key": "elder", "name": "노인돌봄", "basis": BASIS_NATION, "items": [
        ("home_care_per_old_1k", "노인 천 명당 재가노인복지시설 수", "곳"),
        ("care_home_per_old_1k", "노인 천 명당 노인요양시설 수", "곳"),
        ("senior_center_per_old_10k", "노인 만 명당 노인복지관 수", "곳"),
    ]},
    {"key": "infant", "name": "영유아보육", "basis": BASIS_PEER, "items": [
        ("daycare_seats_per_infant_100", "영유아 백 명당 어린이집 정원", "명"),
        ("public_daycare_seat_share", "국공립 어린이집 정원 비율", "%"),
    ]},
    {"key": "child", "name": "아동돌봄", "basis": BASIS_PEER, "items": [
        ("child_center_per_child_10k", "아동 만 명당 지역아동센터 수", "곳"),
        ("care_center_per_child_10k", "아동 만 명당 다함께돌봄센터 수", "곳"),
    ]},
    {"key": "disabled", "name": "장애인·복지", "basis": BASIS_NATION, "items": [
        ("disabled_fac_per_disabled_1k", "등록장애인 천 명당 장애인 시설 수", "곳"),
        ("welfare_center_per_recipient_10k", "기초수급자 만 명당 사회복지관 수", "곳"),
    ]},
    {"key": "library", "name": "도서관", "basis": BASIS_PEER, "items": [
        ("lib_per_100k", "주민 십만 명당 공공도서관 수", "곳"),
        ("librarians_per_100k", "주민 십만 명당 사서 수", "명"),
    ]},
]

def gap_medians(rows):
    medians = {}
    for domain in GAP_DOMAINS:
        for item in domain["items"]:
            key = item[0]
            values = [row[key] for row in rows if key in row]
            if values:
                medians[key] = statistics.median(values)
    return medians

def load_gap(path="data/welfare_gap.csv"):
    rows = []
    str_cols = ["sido", "sigungu", "level_access", "level_medical", "level_elder", "level_infant", "level_child", "level_disabled", "level_library", "access_source", "cluster_name", "library_region"]
    int_cols = ["pop", "map_x", "map_y", "lacking_count", "unsure_count", "no_er", "no_delivery_room", "cluster_unsure", "small_pop", "new_gu", "few_cells"]
    with open(path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_row = {}
            for key, value in row.items():
                if key in str_cols:
                    new_row[key] = value
                elif key in int_cols:
                    new_row[key] = int(value)
                else:
                    new_row[key] = float(value)
            rows.append(new_row)
    return rows

def show_number(value):
    if value == 0:
        return "0"
    elif value < 1:
        return f"{value:.2f}"
    else:
        return f"{value:.1f}"

def gap_notices(rows, card):
    row = None
    for r in rows:
        if r["sido"] == card["sido"] and r["sigungu"] == card["sigungu"]:
            row = r
            break
    
    if row is None:
        return []
        
    notices = []
    
    if row.get("small_pop") == 1:
        notices.append("주민이 3만 명보다 적어, 시설 한 곳 차이로 숫자가 크게 달라집니다.")
        
    if row.get("new_gu") == 1:
        notices.append("2026년에 새로 생긴 구입니다. 어린이집·기초연금 등 일부 값은 옛 구의 값을 인구 비율로 나눈 추정입니다.")
        
    if row.get("few_cells") == 1:
        notices.append("면적이 좁아 거리 값이 거칠게 계산됐습니다.")
        
    for domain in card.get("domains", []):
        if domain.get("level") == "넉넉" and domain.get("key") != "access":
            for item in domain.get("items", []):
                if item.get("raw") == 0:
                    notices.append(f"{domain['name']} 영역은 넉넉으로 나왔지만 '{item['label']}' 값은 0입니다. 다른 지표가 높아 넉넉이 된 것입니다.")
                    
    if row.get("level_access") == "넉넉" and row.get("no_delivery_room") == 1:
        notices.append("의료거리는 차로 가는 시간 기준이라 넉넉으로 나왔습니다. 분만하려면 다른 지역으로 가야 합니다.")
        
    return notices

def top_lacking(rows, n=10):
    sorted_rows = sorted(rows, key=lambda x: (-x["lacking_count"], -x["pop"]))
    result = []
    for row in sorted_rows[:n]:
        result.append({
            "sido": row["sido"],
            "sigungu": row["sigungu"],
            "lacking_count": row["lacking_count"],
            "unsure_count": row["unsure_count"],
            "pop": row["pop"]
        })
    return result

def sido_regions(rows, sido):
    filtered = [row for row in rows if row["sido"] == sido]
    if not filtered:
        return []
    sorted_rows = sorted(filtered, key=lambda x: (-x["lacking_count"], x["sigungu"]))
    result = []
    for row in sorted_rows:
        result.append({
            "sido": row["sido"],
            "sigungu": row["sigungu"],
            "lacking_count": row["lacking_count"],
            "unsure_count": row["unsure_count"],
            "pop": row["pop"]
        })
    return result

def dot_color(lacking_count):
    if lacking_count >= 4:
        return "#c0392b"
    elif lacking_count in [2, 3]:
        return "#e67e22"
    else:
        return "#7f9fc5"

def map_points(rows, sido=None):
    if sido is None:
        target_rows = rows
    else:
        target_rows = [r for r in rows if r["sido"] == sido]
    
    if not target_rows:
        return {"width": 1000, "height": 300, "points": []}
    
    sorted_rows = sorted(target_rows, key=lambda x: (x["lacking_count"], x["sigungu"]))
    
    if sido is None:
        max_y = max(r["map_y"] for r in target_rows)
        height = max_y + 20
        points = []
        for r in sorted_rows:
            points.append({
                "x": r["map_x"],
                "y": r["map_y"],
                "color": dot_color(r["lacking_count"]),
                "sido": r["sido"],
                "sigungu": r["sigungu"],
                "lacking_count": r["lacking_count"]
            })
        return {"width": 1000, "height": height, "points": points}
    else:
        min_x = min(r["map_x"] for r in target_rows)
        max_x = max(r["map_x"] for r in target_rows)
        min_y = min(r["map_y"] for r in target_rows)
        max_y = max(r["map_y"] for r in target_rows)
        
        span = max(max_x - min_x, max_y - min_y, 1)
        scale = 900 / span
        cx = (min_x + max_x) / 2
        cy = (min_y + max_y) / 2
        height = max(300, round(100 + (max_y - min_y) * scale))
        
        points = []
        for r in sorted_rows:
            points.append({
                "x": round(500 + (r["map_x"] - cx) * scale),
                "y": round(height / 2 + (r["map_y"] - cy) * scale),
                "color": dot_color(r["lacking_count"]),
                "sido": r["sido"],
                "sigungu": r["sigungu"],
                "lacking_count": r["lacking_count"]
            })
        return {"width": 1000, "height": height, "points": points}

def build_map_svg(map_data, big=False):
    r = 22 if big else 9
    res = f'<svg viewBox="0 0 {map_data["width"]} {map_data["height"]}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="점 지도">'
    for p in map_data["points"]:
        region = quote(p["sido"] + "|" + p["sigungu"])
        res += f'<a href="/region?region={region}">'
        res += f'<circle cx="{p["x"]}" cy="{p["y"]}" r="{r}" fill="{p["color"]}"><title>{p["sido"]} {p["sigungu"]} · 부족 {p["lacking_count"]}개</title></circle>'
        if big:
            if p["x"] > 780:
                res += f'<text x="{p["x"] - 28}" y="{p["y"] + 10}" font-size="30" text-anchor="end">{p["sigungu"]}</text>'
            else:
                res += f'<text x="{p["x"] + 28}" y="{p["y"] + 10}" font-size="30">{p["sigungu"]}</text>'
        res += '</a>'
    res += '</svg>'
    return res

def gap_fallback_summary(card):
    if card["lacking_count"] == 0:
        return f"{card['sigungu']}의 7개 영역 가운데 부족으로 나온 영역은 없습니다."
    else:
        names = ", ".join(card["lacking_names"])
        return f"{card['sigungu']}의 7개 영역 가운데 {card['lacking_count']}개가 부족으로 나왔습니다. 부족한 영역은 {names}입니다."

def is_safe_gap_summary(text, card):
    if text is None:
        return False
    if not text.strip():
        return False
    if len(text) > 200:
        return False

    allowed = {"7", str(card["lacking_count"])}
    for domain in card.get("domains", []):
        if domain.get("level") == "부족":
            for item in domain.get("items", []):
                allowed.add(item["value"])

    import re
    numbers_in_text = re.findall(r"\d+(?:\.\d+)?", text)
    for num in numbers_in_text:
        if num not in allowed:
            return False

    for domain in card.get("domains", []):
        if domain["name"] in text and domain.get("level") != "부족":
            return False

    return True


def is_good_gap_summary(text, card):
    if not is_safe_gap_summary(text, card):
        return False
    numbers = re.findall(r"\d+(?:\.\d+)?", text)
    if "7" not in numbers:
        return False
    if card["lacking_count"] > 0 and str(card["lacking_count"]) not in numbers:
        return False
    return True