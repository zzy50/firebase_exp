from flask import Flask, send_from_directory
from flask_cors import CORS

HLS_PATH = 'C:/Users/ZZY/Desktop/0_cityeyelab/code/firebase_exp/backend/hls_http/'

app = Flask(__name__)
CORS(app)

@app.route('/hls/<path:filename>')
def serve_hls(filename):
    return send_from_directory(HLS_PATH, filename)

if __name__ == '__main__':
    app.run()