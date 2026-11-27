import csv
import json
import os
import re
import app
import logic

def cut_container(html):
    start_marker = '<div class="container">'
    end_marker = '</div>'
    
    start_idx = html.find(start_marker)
    if start_idx == -1:
        return ""
    
    content_after_start = html[start_idx + len(start_marker):]
    
    last_end_idx = content_after_start.rfind(end_marker)
    if last_end_idx == -1:
        return content_after_start.strip()
    
    result = content_after_start[:last_end_idx]
    return result.strip()

def fix_links(fragment):
    fragment = fragment.replace('href="/region?region=', 'href="#region=')
    fragment = fragment.replace('href="/?sido=', 'href="#sido=')
    fragment = fragment.replace('href="/"', 'href="#"')
    return fragment

def load_summaries(path="data/gap_summaries.csv"):
    if not os.path.exists(path):
        return {}
    
    summaries = {}
    with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row["sido"] + "|" + row["sigungu"]
            value = (row["summary"], row["label"])
            summaries[key] = value
    return summaries

def replace_block(fragment, start_text, new_text):
    start = fragment.find(start_text)
    if start == -1:
        return fragment
    end = fragment.find("</div>", start) + len("</div>")
    return fragment[:start] + new_text + fragment[end:]

def summary_info(card, saved):
    allowed = {"7", str(card["lacking_count"])}
    banned = []
    for domain in card["domains"]:
        if domain["level"] == "부족":
            for item in domain["items"]:
                allowed.add(item["value"])
        else:
            banned.append(domain["name"])
    
    return {
        "prompt": logic.build_gap_prompt(card),
        "saved": saved[0],
        "saved_label": saved[1],
        "allowed": sorted(list(allowed)),
        "banned": banned,
        "count": card["lacking_count"]
    }
