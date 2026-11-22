from flask import Flask, render_template, request
from openai import OpenAI
import logic

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")
app = Flask(__name__)

def ask_gemma(prompt):
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": prompt}])
    return r.choices[0].message.content

def make_summary(card):
    try:
        answer = ask_gemma(logic.build_summary_prompt(card))
        if logic.is_safe_summary(answer, card):
            return (answer.strip(), "AI 요약")
        else:
            return (logic.fallback_summary(card), "기본 요약")
    except Exception:
        return (logic.fallback_summary(card), "기본 요약")

@app.route("/")
def home():
    rows = logic.load_gap()
    sido_list = logic.get_sido_list(rows)
    sido = request.args.get("sido", "")
    if sido in sido_list:
        map_svg = logic.build_map_svg(logic.map_points(rows, sido), True)
        regions = logic.sido_regions(rows, sido)
        message = None
    else:
        map_svg = logic.build_map_svg(logic.map_points(rows))
        regions = logic.top_lacking(rows)
        message = "등록된 지역 정보가 없습니다" if sido else "지역을 선택해주세요"
        sido = ""
    return render_template("home.html", sido_list=sido_list, sido=sido, map_svg=map_svg, regions=regions, message=message)

def make_gap_summary(card):
    try:
        answer = ask_gemma(logic.build_gap_prompt(card))
        if logic.is_safe_gap_summary(answer, card):
            return (answer.strip(), "AI 요약")
        else:
            return (logic.gap_fallback_summary(card), "기본 요약")
    except Exception:
        return (logic.gap_fallback_summary(card), "기본 요약")

@app.route("/region")
def region():
    rows = logic.load_gap()
    value = request.args.get("region", "")
    card = None
    notices = []
    summary = None
    summary_label = None
    if not value:
        message = "지역을 선택해주세요"
    else:
        sido, _, sigungu = value.partition("|")
        card, message = logic.gap_card(rows, sido, sigungu)
        if card:
            notices = logic.gap_notices(rows, card)
            summary, summary_label = make_gap_summary(card)
    return render_template("region.html", card=card, message=message, notices=notices, summary=summary, summary_label=summary_label)

@app.route("/library")
def index():
    rows = logic.load_library()
    sido_list = logic.get_sido_list(rows)
    groups = [(sido, logic.get_sigungu_list(rows, sido)) for sido in sido_list]
    
    region = request.args.get("region", "")
    card = None
    message = None
    summary = None
    summary_label = None
    
    if not region:
        message = "지역을 선택해주세요"
    else:
        sido, _, sigungu = region.partition("|")
        card, message = logic.library_card(rows, sido, sigungu)
        if card:
            summary, summary_label = make_summary(card)
            
    return render_template("index.html", groups=groups, region=region, card=card, message=message, summary=summary, summary_label=summary_label)

@app.route("/smoking")
def smoking():
    return render_template("smoking.html", rows=logic.smoking_priority(logic.load_smoking()))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)