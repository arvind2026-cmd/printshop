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
    return send_file('qr.png', mimetype='image/png')

@app.route('/save', methods=['POST'])
def save():
    file = request.files['photo']
    file.save('print_me.jpg')
    return 'OK'

@app.route('/print', methods=['POST'])
def print_file():
    try:
        os.startfile('print_me.jpg', 'print')
    except:
        pass
    return 'OK'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)