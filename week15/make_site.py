import json
import app
import logic
import build_site

EMPTY_SUMMARY = '<div class="panel summary" id="summary"><strong></strong><p></p></div>'


def build_all(summaries):
    # Flask 화면을 그려 잘라 낸 조각과 지도 색, 요약을 한 dict 로 모은다
    app.ask_gemma = lambda prompt: ""
    client = app.app.test_client()
    rows = logic.load_gap()
    paths = logic.load_map_paths()
    views = logic.load_map_views()
    domain_keys = [""] + [d["key"] for d in logic.GAP_DOMAINS]

    def page(url, query):
        html = client.get(url, query_string=query).get_data(as_text=True)
        return build_site.fix_links(build_site.cut_container(html))

    site = {"home": {}, "regions": {}, "colors": {}, "summary": {}, "legends": {}}
    site["home"][""] = page("/", {})
    for sido in logic.get_sido_list(rows):
        site["home"][sido] = page("/", {"sido": sido})
    for key in domain_keys:
        view = logic.home_view(rows, paths, views, "", key)
        site["legends"][key] = {"legend": view["legend"], "note": view["map_note"]}
    for row in rows:
        key = row["sido"] + "|" + row["sigungu"]
        fragment = page("/region", {"region": key})
        fragment = build_site.replace_block(fragment, '<div class="panel summary">', EMPTY_SUMMARY)
        fragment = build_site.replace_block(fragment, '<div class="btn-row"><a class="btn btn-light" href="/library', "")
        site["regions"][key] = fragment
        site["colors"][key] = {k: logic.area_color(row, k) for k in domain_keys}
        card, _ = logic.gap_card(rows, row["sido"], row["sigungu"])
        saved = summaries.get(key, (logic.gap_fallback_summary(card), "기본 요약"))
        site["summary"][key] = build_site.summary_info(card, saved)
    site["missing"] = page("/region", {"region": "없는도|없는군"})
    return site


def main(path="site_data.js"):
    site = build_all(build_site.load_summaries())
    with open(path, mode="w", encoding="utf-8") as f:
        f.write("const SITE = " + json.dumps(site, ensure_ascii=False) + ";")
    print("화면 조각", len(site["home"]), "+", len(site["regions"]))


if __name__ == "__main__":
    main()