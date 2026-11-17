import base64, json, re
from flask import Flask, render_template, request
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

app = Flask(__name__)

def ask(prompt, image_bytes=None, mime="image/jpeg"):
    content = [{"type": "text", "text": prompt}]
    if image_bytes:
        url = f"data:{mime};base64," + base64.b64encode(image_bytes).decode()
        content.append({"type": "image_url", "image_url": {"url": url}})
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": content}])
    return r.choices[0].message.content

def parse_json(text):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    try:
        return json.loads(m.group(1) if m else text)
    except (json.JSONDecodeError, TypeError):
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    items = None
    people_count = 1

    if request.method == 'POST':
        try:
            people_count = int(request.form.get('people', 1))
            image_file = request.files.get('receipt_image')

            if image_file:
                image_bytes = image_file.read()
                prompt = "영수증에서 항목 이름과 금액을 추출해서 JSON 형식으로 응답해줘. 형식은 [{'item': '항목명', 'amount': 금액}, ...] 형태여야 해. 다른 설명은 하지 말고 오직 JSON 데이터만 출력해."
                response_text = ask(prompt, image_bytes=image_bytes)
                items = parse_json(response_text)

                if items:
                    total_amount = sum(item['amount'] for item in items)
                    if people_count <= 0:
                        error = "인원수는 1명 이상이어야 합니다."
                    else:
                        split_amount = round(total_amount / people_count, 1)
                        result = f"{split_amount:,.1f} 원"
                else:
                    error = "읽지 못했습니다"
            else:
                total_amount = int(request.form.get('amount', 0))
                if people_count <= 0:
                    error = "인원수는 1명 이상이어야 합니다."
                else:
                    split_amount = round(total_amount / people_count, 1)
                    result = f"{split_amount:,.1f} 원"

        except ValueError:
            error = "숫자만 입력해주세요."

    return render_template('index.html', result=result, error=error, items=items, people_count=people_count)

if __name__ == '__main__':
    app.run(debug=True)