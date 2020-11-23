from flask import Flask
from flask import render_template, request, url_for, make_response
from werkzeug.utils import secure_filename
import os
from scripts.delete_files import delete_files
from scripts.instance import init_fun, detect_img
from flask import jsonify
import re
from werkzeug.datastructures import FileStorage
import requests
import shutil

import os
from google.cloud import storage
from io import BytesIO
from PIL import Image

app = Flask(__name__)
yolo_ins = init_fun(app.root_path)

#import pdb; pdb.set_trace()

#CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
CLOUD_STORAGE_BUCKET = 'yolo_data'


@app.route('/status')
def status():
    # import pdb; pdb.set_trace()
    if request.headers.get("Content-Type") == 'application/json':
        return jsonify(status="OK")
    return 'OK'

@app.route('/')
def index(name=None):
    frame = url_for('static', filename='images/frame.jpg')
    return render_template('index.html',
                            name=name,
                            path_upload_image=frame,
                            path_output_image=frame,
                            label="Result")

@app.route('/detection', methods=['POST'])
def detection(name=None):
    # import pdb; pdb.set_trace()

    # delete_files()
    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    if request.headers.get("Content-Type") == 'application/json':
        request_json = request.get_json()
        file_path = request_json.get("image")
        name = re.split(r"/|\\", file_path)[-1]
        response = requests.get(file_path)
        image = Image.open(BytesIO(response.content))

        # Creating the "string" object to use upload_from_string
        img_byte_array = BytesIO()
        image.save(img_byte_array, format='JPEG')

        # Create a new blob and upload the file's content.
        blob = bucket.blob(name)

        blob.upload_from_string(img_byte_array.getvalue(), content_type="image/jpeg")
        # The public URL can be used to directly access the uploaded file via HTTP.
        uploaded_url = blob.public_url


    else:
        uploaded_file = request.files.get('file')
        # Create a new blob and upload the file's content.
        blob = bucket.blob(uploaded_file.filename)

        blob.upload_from_string(
                uploaded_file.read(),
                content_type=uploaded_file.content_type
        )

        # The public URL can be used to directly access the uploaded file via HTTP.
        uploaded_url = blob.public_url
        name = uploaded_file.filename
        
    output_url = detect_img(yolo_ins, uploaded_url, name)
    if request.headers.get("Content-Type") == 'application/json':
        return jsonify(output=output_url)
    response = make_response(render_template('index.html',
                            name='',
                            path_upload_image=uploaded_url,
                            path_output_image=output_url,
                            label="Output image"))
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run(host='0.0.0.0', port='5000')
