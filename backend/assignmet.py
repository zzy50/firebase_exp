import numpy as np
import firebase_admin
import datetime
import time
import yaml
from typing import Dict
from firebase_admin import credentials, db, storage

FIREBASE_CONFIG = "config/firebase_config.yaml"

# rtdb assignment
RTDB_UPLOAD_PATH = "cityeyelab/detected_info/path"

# storage assignment
IMAGE_RTDB_PATH = "cityeyelab/detected_info/image_test"
UPLOADED_FLAG = "is_uploaded"
UPLOADED_PATH_NAME = "uploaded_path"

UPLOAD_PATH = "image_test/test.png"
IMAGE_PATH = "image_test/test.png"


def main():
    FirebaseInit(FIREBASE_CONFIG)

    # rtdb_upload(RTDB_UPLOAD_PATH)
    storage_upload(src_path=IMAGE_PATH, dst_path=UPLOAD_PATH)


def rtdb_upload(dst_path: str):
    """
        dictionary(= json format)를 firebase의 realtime-database로 업로드.

        Parameters
        ---
            dst_path : str
                realtime-database 경로.
    
    """
    rtdb = FirebaseRTDB()
    rtdb_ref = rtdb.reference(dst_path)
    for input_value in test_generator():
        rtdb_ref.update(input_value)
        time.sleep(2)


def storage_upload(src_path: str, dst_path: str=None):
    """
        로컬 파일을 firebase의 storage로 업로드.

        Parameters
        ---
            src_path : str
                Local 경로.
            dst_path : str
                storage 경로. None을 전달받을 경우 src_path와 동일한 path가 지정됨.
    
    """
    rtdb = FirebaseRTDB()
    rtdb_ref = rtdb.reference(IMAGE_RTDB_PATH)
    is_uploaded = rtdb_ref.child(UPLOADED_FLAG).get()
    if not is_uploaded:
        print(f"is_uploaded: {is_uploaded}")
        print("Uploading...")
        storage = FirebaseStorage()
        storage.upload(src_path, dst_path)
        rtdb_ref.update({UPLOADED_FLAG: True})
        rtdb_ref.update({UPLOADED_PATH_NAME: dst_path})
        print("Done!")
    else:
        print(f"is_uploaded: {is_uploaded}")
        print("Done!")


def test_generator():
    frame_num = 0
    while True:
        now_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        frame_num += 1
        yield {frame_num : now_date}
    

class FirebaseInit:
    def __init__(self, yaml_path: str) -> None:
        firebase_config = self.load_yaml(yaml_path)
        auth_file_path = firebase_config["AUTH"]["AUTH_FILE_PATH"]
        self.rtdb_url = firebase_config["URL"]["RTDB_URL"]
        self.storage_url = firebase_config["URL"]["STORAGE_URL"]
        self.cred = credentials.Certificate(auth_file_path)
        firebase_admin.initialize_app(self.cred,{
            "databaseURL": self.rtdb_url,
            "storageBucket": self.storage_url
        })
    
    @staticmethod
    def load_yaml(yaml_path):
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    

class FirebaseRTDB():
    def reference(self, dst_path: str) -> db.Reference:
        return db.reference(dst_path) # db 위치 지정, 기본적으로 가장 상단을 가리킴


class FirebaseStorage():
    def upload(self, src_path: str, dst_path: str=None) -> None:
        if not dst_path:
            dst_path = src_path
        bucket = storage.bucket()
        blob = bucket.blob(dst_path) # storage에 저장되는 파일의 경로 (꼭 로컬 파일 경로와 같을 필요 없음)
        blob.upload_from_filename(src_path) # 로컬 파일의 경로 
        


if __name__ == "__main__":
    main()

