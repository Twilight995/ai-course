import sqlite3

ROWS = [
    # (이름, 회사, 출시 연도, 공개 방식, 종류, 설명)
    ("Claude Fable 5.1", "Anthropic", 2026, "API·서비스로만 이용", "멀티모달", "어려운 추론과 오래 걸리는 에이전트 작업용 Claude. 글과 이미지를 받고 컨텍스트는 100만 토큰"),
    ("Claude Opus 5.5", "Anthropic", 2026, "API·서비스로만 이용", "멀티모달", "긴 코딩 에이전트 작업과 지식 업무용 Claude. 공식 문서가 대부분의 작업에 먼저 권하는 모델"),
    ("Claude Sonnet 5.5", "Anthropic", 2026, "API·서비스로만 이용", "멀티모달", "속도와 성능의 균형을 맞춘 Claude"),
    ("Claude Haiku 5.5", "Anthropic", 2026, "API·서비스로만 이용", "멀티모달", "분류, 추출처럼 많은 양을 빠르게 처리하는 작업용 Claude. 현재 Claude 중 가장 빠르다"),
    ("GPT-6 Astra", "OpenAI", 2026, "API·서비스로만 이용", "멀티모달", "OpenAI가 가장 능력이 높다고 소개하는 모델. 글과 이미지를 받고 컨텍스트는 약 105만 토큰"),
    ("Gemini 4 Argon", "Google", 2026, "API·서비스로만 이용", "멀티모달", "글, 이미지, 영상, 음성, PDF를 받아 글로 답하는 구글의 대형 모델"),
    ("Grok 4.7", "xAI", 2026, "API·서비스로만 이용", "언어", "xAI의 Grok 시리즈 최신 모델. 컨텍스트 50만 토큰"),
    ("Muse Spark", "Meta", 2026, "API·서비스로만 이용", "멀티모달", "Meta Superintelligence Labs의 첫 Muse 모델. meta.ai와 Meta AI 앱에서 쓴다"),
    ("DeepSeek-V4-Pro", "DeepSeek", 2026, "오픈 가중치", "언어", "전체 1.6조 파라미터 중 토큰마다 490억 개만 계산하는 MoE 모델. 컨텍스트 100만 토큰, MIT 라이선스"),
    ("Qwen3.8-27B", "Alibaba", 2026, "오픈 가중치", "멀티모달", "270억 파라미터에 이미지와 영상 이해를 지원하는 알리바바의 오픈 모델. Apache 2.0"),
    ("Mistral Large 4", "Mistral AI", 2026, "오픈 가중치", "멀티모달", "Mistral의 오픈 가중치 범용 멀티모달 모델"),
    ("Kimi K3", "Moonshot AI", 2026, "오픈 가중치", "멀티모달", "전체 2.8조 파라미터의 MoE 모델. 자체 Kimi K3 라이선스"),
    ("GLM-5.3", "Zhipu AI", 2026, "오픈 가중치", "언어", "7530억 파라미터 언어 모델. GLM-5.2를 추가 학습해 개선했다"),
    ("EXAONE 4.5 33B", "LG AI연구원", 2026, "오픈 가중치", "멀티모달", "한국어를 지원하는 LG의 330억 파라미터 이미지-텍스트 모델. 비상업용 라이선스"),
    ("HyperCLOVA X SEED 32B Think", "Naver", 2025, "오픈 가중치", "멀티모달", "한국어에 강한 HyperCLOVA X 계열의 320억 파라미터 추론 모델. 글, 이미지, 영상을 받는다"),
    ("A.X K1", "SK텔레콤", 2026, "오픈 가중치", "언어", "SK텔레콤이 만든 MoE 언어 모델. 전체 5190억 파라미터, Apache 2.0"),
    ("Gemma 4 E4B", "Google", 2026, "오픈 가중치", "멀티모달", "Gemma 4의 작은 모델. 유효 45억 파라미터로 글, 이미지, 음성을 받는다. Apache 2.0"),
    ("gpt-oss-20b", "OpenAI", 2025, "오픈 가중치", "언어", "OpenAI의 오픈 가중치 언어 모델. 16GB 메모리에서 돌아간다. Apache 2.0"),
    ("Phi-4-mini-instruct", "Microsoft", 2025, "오픈 가중치", "언어", "약 38억 파라미터의 작은 언어 모델. MIT 라이선스"),
    ("GPT-Image-2.5 Sunburst", "OpenAI", 2026, "API·서비스로만 이용", "이미지", "OpenAI의 이미지 생성과 편집 모델. 글과 이미지를 받아 이미지를 만든다"),
    ("Nano Banana 2.1", "Google", 2026, "API·서비스로만 이용", "이미지", "구글의 이미지 생성 모델. 4K까지 출력하고 참조 이미지를 최대 10개 쓸 수 있다"),
    ("FLUX.2 [dev]", "Black Forest Labs", 2025, "오픈 가중치", "이미지", "320억 파라미터 이미지 생성 모델. 참조 이미지로 편집할 수 있다. 비상업용 라이선스"),
    ("Gemini Omni Flash", "Google", 2026, "API·서비스로만 이용", "영상", "글과 이미지로 3~10초 영상을 만들고 대화로 고쳐 쓰는 모델"),
    ("Kling 4.0", "Kuaishou", 2026, "API·서비스로만 이용", "영상", "Kling AI의 영상 생성 모델. 영상과 소리를 함께 만든다"),
    ("Gemini 3.5 Transcribe", "Google", 2026, "API·서비스로만 이용", "음성", "음성을 글자로 바꾸는 모델. 85개 이상 언어, 화자 구분과 단어별 시간 표시 지원"),
    ("Voxtral Mini 3B (2507)", "Mistral AI", 2025, "오픈 가중치", "음성", "음성 인식, 요약, 질의응답을 하는 30억 파라미터 모델. 8개 언어, Apache 2.0"),
    ("Lyria 3.5", "Google", 2026, "API·서비스로만 이용", "음악", "절, 후렴, 브리지가 있는 곡 전체를 만드는 구글의 음악 생성 모델"),
    ("Gemini Embedding 2", "Google", 2026, "API·서비스로만 이용", "임베딩", "글, 이미지, 영상, 음성, PDF를 한 벡터 공간에 넣는 구글의 첫 멀티모달 임베딩 모델"),
    ("Qwen3-Embedding-8B", "Alibaba", 2025, "오픈 가중치", "임베딩", "80억 파라미터 문장 임베딩 모델. 100개 이상 언어, 최대 4096차원, Apache 2.0"),
    ("Qwen3-Coder-480B-A35B-Instruct", "Alibaba", 2025, "오픈 가중치", "코드", "코딩 특화 MoE 모델. 전체 4800억 파라미터 중 토큰마다 350억 개만 계산. Apache 2.0"),
    ("Devstral Small 1.0", "Mistral AI", 2025, "오픈 가중치", "코드", "소프트웨어 개발 에이전트용 240억 파라미터 모델. Apache 2.0"),
    ("Sora 2", "OpenAI", 2025, "서비스 종료", "영상", "OpenAI의 영상 생성 모델. 2026년 9월 24일 API에서 종료되어 지금은 쓸 수 없다"),
    ("Claude Opus 4.1", "Anthropic", 2025, "서비스 종료", "멀티모달", "2026년 8월 5일 종료된 이전 세대 Claude. 권장 대체 모델은 Claude Opus 4.8"),
]

con = sqlite3.connect("campus.db")
con.execute("DROP TABLE IF EXISTS model")
con.execute("""CREATE TABLE model (
    id INTEGER PRIMARY KEY,
    name TEXT, company TEXT, year INTEGER, access TEXT, kind TEXT, description TEXT
)""")
con.executemany("INSERT INTO model (name, company, year, access, kind, description) VALUES (?, ?, ?, ?, ?, ?)", ROWS)
con.commit()
print(con.execute("SELECT COUNT(*) FROM model").fetchone()[0], "행")
