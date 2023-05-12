from flask import Flask, Response
from google.cloud import storage

AUTH_KEY = "auth/firebase_cloud-storage_authkey.json"

app = Flask(__name__)
client = storage.Client.from_service_account_json(AUTH_KEY)
bucket = client.get_bucket('my-bucket')

@app.route('/hls/<path:filename>')
def serve_hls(filename):
    blob = bucket.get_blob(filename)
    if not blob:
        return 'Not found', 404
    content = blob.download_as_string()
    return Response(content, content_type=blob.content_type)

if __name__ == '__main__':
    app.run()