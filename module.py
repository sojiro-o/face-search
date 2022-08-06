import os
from tqdm import tqdm
import face_recognition
import sqlite3
import ngtpy
from PIL import Image

def get_vector(file):
	# file: request.files['file']で受け取ったオブジェクト
	# listに変換する場合は.tolist()が必要
	image_data = face_recognition.load_image_file(file)
	location = face_recognition.face_locations(image_data)
	if len(location) == 1:
		# 顔が認識された場合
		face_vector = face_recognition.face_encodings(image_data, known_face_locations=location)[0]
		return face_vector
	else:
		# 顔が認識されなかった場合
		return 'Sorry I could not detect the face from this image'


def ngt_search(file, ngt_index_path):
	# filerequest.files['file']で受け取るオブジェクト
	vector = get_vector(file)
	if type(vector) is str:
		return vector # 'Sorry I could not detect the face from this image'
	
	ngt_index = ngtpy.Index(ngt_index_path, zero_based_numbering=False)
	face_db = sqlite3.connect('./data/face_db.db')
	cur_face_db = face_db.cursor()
	size = 10 # 上位10人まで検索
	index_id_of_similar = [i[0] for i in ngt_index.search(vector.tolist(), size)] # ngt_index.search = [[index_id, 類似度(L2ではロス)], ]類似度の昇順

	ID_of_similar = []
	for index_id in index_id_of_similar:
		cur_face_db.execute("SELECT * FROM face_db WHERE index_id = (?)", (index_id, ))
		a = cur_face_db.fetchone()[1]
		ID_of_similar.append(a)
	face_db.close()

	return ID_of_similar


def register(ID, file):
	# file: request.files['file']で受け取ったオブジェクト
	face_db = sqlite3.connect('./data/face_db.db')
	cur_face_db = face_db.cursor()
	cur_face_db.execute("SELECT COUNT(*) FROM face_db WHERE ID = (?)", (str(ID),)) # 検索の実行
	if cur_face_db.fetchone()[0] == 1:
		# IDが既に存在する場合
		face_db.close()
		return "This ID is already registered"
	else:
		# 新たに登録する場合
		vector = get_vector(file)
		if type(vector) is str:
			# 送られた画像から顔が認識できない場合
			return vector # 'Sorry I could not detect the face from this image'
		
		img = Image.open(file)
		img.save("./data/storage/{}.jpg".format(ID)) # 画像を保存
		
		if not os.path.isfile('./data/index'):
			# ngtのindexがない場合は作る
			ngtpy.create(path='./data/index', dimension=128, distance_type="L2")
		index = ngtpy.Index('./data/index', zero_based_numbering=False)
		index.insert(vector.tolist()) # リスト型に変更
		index.build_index() 
		index.save() # indexに登録
		face_db.execute("INSERT INTO face_db(ID) values(?)", (str(ID),))
		face_db.commit() # DBにも挿入
		face_db.close()
		return "registered new ID and photo"


def register_folder(folder):
    # folder: ID.jpgの形式で画像が格納されたディレクトリパス
    failed_list = [] # 顔の認識ができず取り込みが失敗した画像ID名
    already_registered = []

    objects = [] # 登録するベクトルをまとめたリスト
    face_db = sqlite3.connect('./data/face_db.db')
    cur_face_db = face_db.cursor()
    files = os.listdir(folder)

    if not os.path.isfile('./data/index'):
        # ngtのindexがない場合は作る
        ngtpy.create(path='./data/index', dimension=128, distance_type="L2")
    index = ngtpy.Index('./data/index', zero_based_numbering=False)

    for file in tqdm(files):
        ID = os.path.splitext(os.path.basename(file))[0]
        cur_face_db.execute("SELECT COUNT(*) FROM face_db WHERE ID = (?)", (str(ID),)) # 検索の実行
        
        if cur_face_db.fetchone()[0] == 1:
            # IDが既に存在する場合
            already_registered.append(ID)
            continue
        
        # 新たに登録する場合
        vector = get_vector("{}/{}".format(folder, file))
        if type(vector) is str:
            # 顔認識が失敗した場合
            failed_list.append(ID)
            continue 
        
        # 要変更
        img = Image.open("{}/{}".format(folder, file))
        img.save("./data/storage/{}.jpg".format(ID)) # 画像を保存

        objects.append(vector.tolist())
        cur_face_db.execute("INSERT INTO face_db(ID) values(?)", (str(ID),)) # DBにはIDのみ挿入
    if len(objects):
        index.batch_insert(objects) # indexにobjectsを挿入
    index.save()
    face_db.commit() # DBの更新を保存
    face_db.close()
    print("already registered", *already_registered)
    print("can not save:", *failed_list)