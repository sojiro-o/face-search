import json
import unittest
import io
import api_server


class TestFlasker(unittest.TestCase):
    def setUp(self):
        self.app = api_server.app.test_client()
        self.oid = None

    def test_01_status(self):
        response = self.app.get("/status")
        assert response.status_code == 200
        print(response.get_data(as_text=True))
        out = json.loads(response.get_data(as_text=True))
        assert out["status"] == "ok"

    def test_02_predict_get(self):
        get_response = self.app.get("/")
        assert get_response.status_code == 200

    def test_03_predict_jpg_post(self):
        with open("./data/test_images/215069.jpg", 'rb') as f:
            binary = f.read()
        post_response = self.app.post("/", data={"file" :  (io.BytesIO(binary), "test.jpg")}, content_type='multipart/form-data')
        assert post_response.status_code == 200

    def test_04_predict_nofile_post(self):
        no_file_response = self.app.post("/", data={"file" : None}, content_type='multipart/form-data')
        assert no_file_response.json["message"] is not None
        assert no_file_response.status_code == 200

    def test_05_predict_notjpg_post(self):
        not_image_response = self.app.post("/", data={"file" :  (io.BytesIO(b"test"), "test.txt")}, content_type='multipart/form-data')
        assert not_image_response.json["message"] is not None
        assert not_image_response.status_code == 200

    def test_06_upload_get(self):
        get_response = self.app.get("/upload")
        assert get_response.status_code == 200
    
    def test_07_upload_jpg_post(self):
        with open("./data/test_images/215069.jpg", 'rb') as f:
            binary = f.read()
        post_response = self.app.post("/upload", data={"file" :  (io.BytesIO(binary), "test.jpg")}, content_type='multipart/form-data')
        assert post_response.status_code == 200

    def test_08_upload_nofile_post(self):
        no_file_response = self.app.post("/upload", data={"file" : None}, content_type='multipart/form-data')
        assert no_file_response.json["message"] is not None
        assert no_file_response.status_code == 200

    def test_09_upload_notjpg_post(self):
        not_image_response = self.app.post("/upload", data={"file" :  (io.BytesIO(b"test"), "test.txt")}, content_type='multipart/form-data')
        assert not_image_response.json["message"] is not None
        assert not_image_response.status_code == 200