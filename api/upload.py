import os
from flask import Blueprint, request, jsonify
import json

# 自作関数
from module import register

upload = Blueprint('upload', __name__)

@upload.route("/upload", methods=['GET', 'POST'])
def process():
    if request.method == 'GET':
        return """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>

            <form class="form-signin" method=post enctype=multipart/form-data>
                <h1 class="h3 mb-3 font-weight-normal">Upload a face image to be registered (Format: ID.jpg)</h1>
                <input type="file" name="file" class="form-control-file" id="inputfile">
                <br/>
                <button class="btn btn-lg btn-primary btn-block" type="submit">Upload</button>
            </form>

        </body>
        </html>"""
    if request.method == 'POST':
        try:
            if ("file" not in request.files) or ("" == request.files["file"].filename):
                return jsonify(status="error", message='No images selected for upload')
            file = request.files['file']
            if (not file.mimetype=="image/jpeg") and (not file.mimetype=="image/png"):
                return jsonify(status="error", message='Only jpg,png files are supported')
            ID = os.path.splitext(os.path.basename(file.filename))[0]
            result = register(ID, file)
            return jsonify(status="ok", result=result)
        except:
            return jsonify(status="error", message='An unexpected error has occurred')
