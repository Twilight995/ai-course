import os
import base64
import json
import requests
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='.')

SECRET_KEY = os.environ.get('TOSS_SECRET_KEY', 'test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    payment_key = request.args.get('paymentKey')
    order_id = request.args.get('orderId')
    amount = request.args.get('amount')

    # 1. Validate amount
    if int(amount) != 1000:
        return render_template('success.html', error={'code': 'INVALID_AMOUNT', 'message': f'Expected 1000, but got {amount}'}), 400

    # 2. Call Toss Payments Approval API
    auth_header = base64.b64encode(f"{SECRET_KEY}:".encode()).decode()
    url = f"https://api.tosspayments.com/v1/payments/{payment_key}/confirm"
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/json"
    }
    payload = {
        "orderId": order_id,
        "amount": int(amount)
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            # Success
            return render_template('success.html', 
                                   result=response_data, 
                                   result_json=json.dumps(response_data, indent=2, ensure_ascii=False))
        else:
            # Failure
            return render_template('success.html', error=response_data), response.status_code

    except Exception as e:
        return render_template('success.html', error={'code': 'SERVER_ERROR', 'message': str(e)}), 500

@app.route('/fail')
def fail():
    code = request.args.get('code')
    message = request.args.get('message')
    return render_template('fail.html', code=code, message=message)

if __name__ == '__main__':
    app.run(port=5000, debug=True)