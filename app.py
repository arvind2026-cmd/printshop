from flask import Flask, request, send_file, make_response
import os
import hmac
import hashlib

app = Flask(__name__)

RAZORPAY_SECRET = "printshop123"

@app.route('/')
def home():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    response = make_response(content)
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

@app.route('/qr')
def qr():
    return send_file('qr.png', mimetype='image/png')

@app.route('/save', methods=['POST'])
def save():
    file = request.files['photo']
    file.save('C:\\printshop\\print_me.jpg')
    return 'OK'

@app.route('/webhook', methods=['POST'])
def webhook():
    # Razorpay signature verify karo
    received_sig = request.headers.get('X-Razorpay-Signature', '')
    body = request.get_data()
    
    expected_sig = hmac.new(
        RAZORPAY_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if hmac.compare_digest(received_sig, expected_sig):
        data = request.json
        event = data.get('event', '')
        print("EVENT:", event)
        
        if event == 'payment.captured':
            print("PAYMENT HO GAYA - PRINT HO RAHA HAI!")
            try:
                os.startfile('C:\\printshop\\print_me.jpg', 'print')
            except Exception as e:
                print("Print Error:", e)
        return 'OK', 200
    else:
        print("SIGNATURE GALAT HAI!")
        return 'Unauthorized', 401

@app.route('/print', methods=['POST'])
def print_file():
    try:
        os.startfile('C:\\printshop\\print_me.jpg', 'print')
    except:
        pass
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)