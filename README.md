# face search
<div align="center">
<img src="./data/readme/title.png" width="80%">
</div>
<p align="center">
  <a href="https://github.com/yahoojapan/NGT/blob/master/python/README-ngtpy-jp.md"><img src="https://raw.githubusercontent.com/yahoojapan/NGT/b84312870d496d0f4e3ead449bc6424545d9f896/assets/logo.svg" height="50px;" /></a>
  <a href="https://github.com/ageitgey/face_recognition"><img src="https://cloud.githubusercontent.com/assets/896692/23625227/42c65360-025d-11e7-94ea-b12f28cb34b4.png" height="50px;" /></a>
</p>

## ð æ¦è¦ 
[face_recognition](https://github.com/ageitgey/face_recognition) ã¨ [ngt](https://github.com/yahoojapan/NGT/blob/master/python/README-ngtpy-jp.md) ãå©ç¨ãããã£ããããæ¤ç´¢API

## ð æºå
ãªãã¸ããªãã¯ã­ã¼ã³ã, ./face-search/data/first_upload_images ã«ãã£ã¬ã¯ããªãä½ã IDå.jpg ã®å½¢å¼ã§ç»åãä¿å­. ããã«ããç»åã¯æå (docker run) ããç»é²ããã.
<br>ãã£ã¬ã¯ããª face-search ã«ç§»å Dockerfile ãã build.
```bash
git clone https://github.com/sojiro-otsubo/face-search.git
# ./face-search/data/first_upload_imagesãã£ã¬ã¯ããªãä½ã
# ./face-search/data/first_upload_images ã«ç»åè¿½å 
cd face-search
docker build -t api_test .
```

## ð apiã®èµ·å
```bash
docker run --gpus all --name faceAPI -p 5000:5000 -it api_test
ð http://localhost:5000
```

## ð¬ apiã®ä½¿ãæ¹
### ***@predict.route("/", methods=['GET', 'POST'])***

ãã£ãããããæ¤ç´¢ãããäººã® jpg ã png ã¤ã¡ã¼ã¸ãã¢ããã­ã¼ãããã¨, ãã£ããåº¦ä¸ä½10ä½ã®IDã jsonå½¢å¼ã§è¿ããã.
<div align="center">
<img src="./data/readme/predict.jpg" width="50%">
</div>

```
{"result":["000034","000019","000002","000024","000064","000012","000030","000022","000037","000016"],"status":"ok"}
```

### ***@upload.route("/upload", methods=['GET', 'POST'])***
ãã¼ã¿ãã¼ã¹ã«ç»é²ãããäººã® jpg ã png ã¤ã¡ã¼ã¸ã IDå.jpg ã®å½¢å¼ã§ã¢ããã­ã¼ãããã¨, data/face_db.db, data/index ã¸ã®ç»é², storageã¸ã®ç»åã®ä¿å­ãè¡ããã.

### ***@status.route('/status')***
æ­»æ´»ãã§ãã¯

## ð¯ apiã®ãã¹ã
```bash
docker run -t api_test python3 -m unittest tests.test_api
```

## ð è¨­è¨
ngtãç¹æã®æ¢ç´¢ã¢ã«ã´ãªãºã ãå©ç¨ãã¦ãããã, indexã«ã¯ãã¯ãã«ã¨ãã®ãã¯ãã«ãæ ¼ç´ããé çªããä¿å­ããã¦ããªã. æ¤ç´¢ã¨ã¡ã¿ãã¼ã¿ãç´ã¥ãããã, indexã«ãã¯ãã«ãæ¿å¥ããã®ã¨åæã«DBã«ãã¼ã¿ã¨ã¡ã¿ãã¼ã¿ãæ¿å¥ãã. 
