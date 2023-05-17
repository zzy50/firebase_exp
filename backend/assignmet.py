import numpy as np
import firebase_admin
import datetime
import time
from typing import Dict
from firebase_admin import credentials
from firebase_admin import db

AUTH_FILE_PATH = "auth/firebase_realtime-database_authkey.json"
DB_URL = "https://backend-test-db3f5-default-rtdb.firebaseio.com/"

def main():
    firebase = FirebaseInit(auth_file_path=AUTH_FILE_PATH, databseURL=DB_URL)
    ref = firebase.get_reference("cityeyelab/detected_info/current_frame_test")
    for input_value in test_generator():
        ref.update(input_value)
        time.sleep(2)


class FirebaseInit:
    def __init__(self, auth_file_path: str, databseURL: str) -> None:
        cred = credentials.Certificate(auth_file_path)
        self.app = firebase_admin.initialize_app(cred, {
            "databaseURL": databseURL
        })
        
    def get_reference(self, path: str="cityeyelab/detected_info") -> db.Reference:
        return db.reference(path, self.app) # db 위치 지정, 기본적으로 가장 상단을 가리킴


def test_generator():
    frame_num = 0
    while True:
        now_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        frame_num += 1
        yield {frame_num : now_date}
    
    
if __name__ == "__main__":
    main()

