from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Version 2 - This will fail!</h1>"

@app.route('/health')
def health():
    return "ERROR", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
