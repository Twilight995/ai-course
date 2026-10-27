import sqlite3
import ollama
import numpy as np

con = sqlite3.connect("campus.db")
rows = con.execute("SELECT id, name, embedding FROM model").fetchall()
names = [r[1] for r in rows]
V = np.stack([np.frombuffer(r[2], dtype=np.float32) for r in rows])
V = V / np.linalg.norm(V, axis=1, keepdims=True)

# (질문, 정답 모델 이름)
TESTS = [
    ("그림 그려 주는 AI 중에 내 컴퓨터에 받아서 쓸 수 있는 거?", "FLUX.2 [dev]"),
    ("말하는 사람을 구분해서 받아 적어 주는 모델은?", "Gemini 3.5 Transcribe"),
    ("노래 한 곡을 통째로 만들어 주는 AI", "Lyria 3.5"),
    ("이동통신사가 만든 언어 모델은?", "A.X K1"),
    ("구글이 낸 작은 오픈 모델 중에 음성도 알아듣는 거", "Gemma 4 E4B"),
    ("이제는 쓸 수 없게 된 동영상 생성 AI", "Sora 2"),
    ("프로그래밍 에이전트용으로 만든 작은 오픈 모델", "Devstral Small 1.0"),
    ("사진이랑 영상까지 같은 공간에 넣는 임베딩", "Gemini Embedding 2"),
    ("LG에서 만든 AI 알려줘", "EXAONE 4.5 33B"),
    ("대량으로 빠르게 분류할 때 쓰는 Claude", "Claude Haiku 5.5"),
]

hit1 = hit3 = 0
for q, want in TESTS:
    qv = np.array(ollama.embed(model="bge-m3", input=q).embeddings[0])
    qv = qv / np.linalg.norm(qv)
    top = [names[i] for i in np.argsort(-(V @ qv))[:3]]
    ok1, ok3 = top[0] == want, want in top
    hit1 += ok1
    hit3 += ok3
    print("O" if ok1 else ("△" if ok3 else "X"), q, "->", top[0], "" if ok1 else f"(정답 {want}, 3위 안 {ok3})")
print(f"\n1위 적중 {hit1}/{len(TESTS)}, 3위 안 적중 {hit3}/{len(TESTS)}")
