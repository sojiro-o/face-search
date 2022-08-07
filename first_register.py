import os
import sqlite3
from tqdm import tqdm
import ngtpy
import face_recognition

# 自作関数
from module import register_folder


# dbにアクセスする. 存在しない場合はdbを作成する.
face_db = sqlite3.connect('./data/face_db.db')
face_db.execute('''
CREATE TABLE IF NOT EXISTS face_db (
	index_id INTEGER PRIMARY KEY, 
	ID TEXT
);
''')
face_db.commit()
face_db.close()

# first_upload_images内の画像を全て登録
register_folder("./data/first_upload_images")
