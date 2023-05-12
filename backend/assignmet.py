import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

AUTH_FILE_PATH = "auth/firebase_authkey.json"
databseURL = "https://backend-test-db3f5-default-rtdb.firebaseio.com/"

new_path = "citeyeylab/first_path"
new_data = [
    {"image": np.zeros((20,20)).tolist()},
    {"frame": 1},
    {"bbox": (200, 100, 600, 200)}
    ]


ref = db.reference(new_path) # db 위치 지정, 기본적으로 가장 상단을 가리킴
for data in new_data:
    ref.update(data)


class FirebaseInit:
    def __init__(self, auth_file_path: str, databseURL: str) -> None:
        cred = credentials.Certificate(auth_file_path)
        firebase_admin.initialize_app(cred, {
            "databaseURL": databseURL
        })
        
 
