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

app = Flask(__name__)
yolo_ins = init_fun(app.root_path)

#import pdb; pdb.set_trace()




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

    delete_files()
    if request.headers.get("Content-Type") == 'application/json':
        request_json = request.get_json()
        file_path = request_json.get("image")
        file_name = re.split(r"/|\\", file_path)[-1]
        response = requests.get(file_path, stream=True)
        # import pdb; pdb.set_trace()
        if response.status_code == 200:
            response.raw.decode_content = True

            new_path_image = os.path.join(app.root_path, 'static', 'images', 'upload', file_name)
            with open(new_path_image, 'wb') as fp:
                shutil.copyfileobj(response.raw, fp)

        # return jsonify(output=path_output_image)

    else:
        file = request.files['file']
        file_name = secure_filename(file.filename)
        new_path_image = os.path.join(app.root_path, 'static', 'images', 'upload', file_name)
        new_outpath_image = os.path.join(app.root_path, 'static', 'images', 'detections', file_name)
        file.save(new_path_image)
        path_upload_image = url_for('static', filename='images/upload/{}'.format(file_name))

    #import pdb; pdb.set_trace()
    detect_img(yolo_ins, new_path_image, new_outpath_image)
    path_output_image = url_for('static', filename='images/detections/{}'.format(file_name))

    if request.headers.get("Content-Type") == 'application/json':
        return jsonify(output="http://localhost:5000" + path_output_image)

    response = make_response(render_template('index.html',
                            name='',
                            path_upload_image=path_upload_image,
                            path_output_image=path_output_image,
                            label="Output image"))

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
