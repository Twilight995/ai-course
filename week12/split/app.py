from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        try:
            total_amount = int(request.form.get('amount', 0))
            people_count = int(request.form.get('people', 0))
            
            if people_count <= 0:
                error = "인원수는 1명 이상이어야 합니다."
            else:
                # 1인당 금액 계산 (소수점 첫째자리까지 반올림)
                split_amount = round(total_amount / people_count, 1)
                result = f"{split_amount:,.1f} 원"
        except ValueError:
            error = "숫자만 입력해주세요."
            
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)