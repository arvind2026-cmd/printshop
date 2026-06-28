from flask import Flask, request, send_file, make_response
import os

app = Flask(__name__)

@app.route('/')
def home():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    response = make_response(content)
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

@app.route('/qr')
def qr():
    return send_file('C:\\printshop\\qr.png', mimetype='image/png')

@app.route('/save', methods=['POST'])
def save():
    file = request.files['photo']
    file.save('C:\\printshop\\print_me.jpg')
    os.startfile('C:\\printshop\\print_me.jpg', 'print')
    return 'OK'

@app.route('/print', methods=['POST'])
def print_file():
    os.startfile('C:\\printshop\\print_me.jpg', 'print')
    return 'OK'

app.run(host='0.0.0.0', port=5000)