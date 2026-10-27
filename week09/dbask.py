import sys
import sqlite3
import ollama
import numpy as np
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")
con = sqlite3.connect("campus.db")

rows = con.execute("SELECT id, name, company, year, access, kind, description, embedding FROM model").fetchall()
V = np.stack([np.frombuffer(r[-1], dtype=np.float32) for r in rows])
V = V / np.linalg.norm(V, axis=1, keepdims=True)


def search(question, k=3):
    q = np.array(ollama.embed(model="bge-m3", input=question).embeddings[0])
    q = q / np.linalg.norm(q)
    sims = V @ q
    return [(float(sims[i]), rows[i][:-1]) for i in np.argsort(-sims)[:k]]


def answer(question):
    found = search(question)
    context = "\n".join(f"- {name} ({company}, {year}년, {kind}, {access}): {desc}"
                        for _, (id_, name, company, year, access, kind, desc) in found)
    prompt = f"""아래 AI 모델 목록만 근거로 질문에 답한다. 목록에 없는 내용은 "자료에 없습니다"라고 답한다. 답은 두 문장 이내로 쓴다.

AI 모델 목록:
{context}

질문: {question}"""
    r = client.chat.completions.create(model="gemma4", temperature=0,
                                       messages=[{"role": "user", "content": prompt}])
    return found, r.choices[0].message.content.strip()


questions = sys.argv[1:] or [
    "그림 그려 주는 AI 중에 내 컴퓨터에서 돌릴 수 있는 거 있어?",
    "회의 녹음을 글로 받아 적어 주는 모델은?",
    "한국 회사가 만든 언어 모델 알려줘",
    "OpenAI가 공개한 오픈 모델 있어?",
    "날씨 예보해 주는 AI는 뭐가 있어?",
]
for q in questions:
    found, a = answer(q)
    print("Q:", q)
    for s, (id_, name, *_rest) in found:
        print(f"   {s:.3f} {name}")
    print("   답:", a)
    print()
