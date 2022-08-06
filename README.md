# [face_recognition](https://github.com/ageitgey/face_recognition) と [ngt](https://github.com/yahoojapan/NGT/blob/master/python/README-ngtpy-jp.md) を利用したそっくりさん検索アプリ

## 準備
リポジトリをクローンし, ./face_search/data/first_upload_images に ID名.jpg の形式で画像を保存. ここにある画像は最初 (docker run) から登録される.
<br>ディレクトリ face_search に移動 Dockerfile より build.
```bash
git clone https://github.com/sojiro-otsubo/face_search.git
# ./face_search/data/first_upload_images に画像追加
cd face_search
docker build -t api_test .
```

## apiの起動
```bash
docker run --gpus all --name faceAPI -p 80:80 -it api_test
```
## apiの使い方
### ***@predict.route("/", methods=['GET', 'POST'])***
そっくりさんを検索したい人の jpg か png イメージをアップロードすると, そっくり度上位10のIDが返される.

### ***@upload.route("/upload", methods=['GET', 'POST'])***
データベースに登録したい人の jpg か png イメージを ID名.jpg の形式でアップロードすると, data/face_db.db, data/index への登録, storageへの画像の保存が行われる.

### ***@status.route('/status')***
死活チェック

## apiのテスト
```bash
docker run -t api_test python3 -m unittest tests.test_api
```

