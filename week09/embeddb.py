import sqlite3
import ollama
import numpy as np

con = sqlite3.connect("campus.db")
columns = [c[1] for c in con.execute("PRAGMA table_info(model)")]
if "embedding" not in columns:
    con.execute("ALTER TABLE model ADD COLUMN embedding BLOB")


# 공개 방식을 사람이 묻는 말로 풀어 쓴다
ACCESS_TEXT = {
    "오픈 가중치": "가중치를 내려받아 내 컴퓨터에서 돌릴 수 있다",
    "API·서비스로만 이용": "인터넷 서비스나 API로만 쓸 수 있다",
    "서비스 종료": "서비스가 끝나 지금은 쓸 수 없다",
}


def row_to_text(name, company, year, access, kind, description):
    return f"{name}. {company} {year}년. {kind} 모델. {ACCESS_TEXT.get(access, access)}. {description}"


rows = con.execute("SELECT id, name, company, year, access, kind, description FROM model").fetchall()
for i, (id_, *fields) in enumerate(rows):
    text = row_to_text(*fields)
    v = np.array(ollama.embed(model="bge-m3", input=text).embeddings[0], dtype=np.float32)
    con.execute("UPDATE model SET embedding = ? WHERE id = ?", (v.tobytes(), id_))
    print(f"\r{i + 1}/{len(rows)} {text[:40]}", end="   ")
con.commit()
print("\n완료")
print("예:", row_to_text(*rows[0][1:]))
