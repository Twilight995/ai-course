import csv
import app
import logic

SAVED_LABEL = "AI 요약 (미리 받아 둔 글)"

def fetch_one(card, tries=3):
    for _ in range(tries):
        text, label = app.make_gap_summary(card)
        if label == "AI 요약":
            return text, SAVED_LABEL
    return logic.gap_fallback_summary(card), "기본 요약"

def main(path="data/gap_summaries.csv"):
    rows = logic.load_gap()
    with open(path, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sido", "sigungu", "summary", "label"])
        for i, row in enumerate(rows, 1):
            card, _ = logic.gap_card(rows, row["sido"], row["sigungu"])
            summary, label = fetch_one(card)
            writer.writerow([row["sido"], row["sigungu"], summary, label])
            print(f"{i} / {len(rows)} {row['sido']} {row['sigungu']} · {label}")

if __name__ == "__main__":
    main()