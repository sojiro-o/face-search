import os
from flask import Blueprint, request, jsonify
import json

# 自作関数
from module import get_vector, ngt_search

predict = Blueprint('predict', __name__)

@predict.route("/", methods=['GET', 'POST'])
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
                <h1 class="h3 mb-3 font-weight-normal">Upload a face image</h1>
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
            ngt_list = ngt_search(file)
            return jsonify(status="ok", result=ngt_list)
        except:
            return jsonify(status="error", message='An unexpected error has occurred')
