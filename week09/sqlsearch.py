import sqlite3

con = sqlite3.connect("campus.db")
for kw in ["이미지", "노트북", "한국어", "녹음"]:
    rows = con.execute("SELECT name FROM model WHERE name LIKE ? OR description LIKE ?",
                       (f"%{kw}%", f"%{kw}%")).fetchall()
    print(kw, [r[0] for r in rows])
