import createdb
from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from flask import json

from werkzeug import secure_filename

app = Flask(__name__)
@app.route('/')
@app.route('/login', methods=["POST"])
def login_user():
    return_val = ''
    formData = request.form
    jsonParams = json.loads(formData.get('user'))
    print('login params',jsonParams)
    try:
        return_val = createdb.login_user(jsonParams['email'], jsonParams['password'])
    except Exception as e:
        print('error ; ', e)
        return_val = 'error'
    return return_val


@app.route('/register', methods=["POST"])
def insert_user():
    return_val = ''

    try:
        if request.method == 'POST':
            formData = request.form
            jsonParams = json.loads(formData.get('user'))
            print('jsonParams: ', jsonParams)
            print('jsonParams: ', jsonParams.get('name'))
            print('jsonParams: ', type(jsonParams))
            name = jsonParams['name']
            print('name: ', name);
            email = jsonParams['email']
            phone_no = jsonParams['mobile']
            print('phone_no: ', phone_no);
            password = jsonParams['password']
            print('password: ', password);

            return_val = createdb.insert_user(name, email, phone_no, password)
    except Exception as e:
        print(e, "something went wrong")
        return_val = 'error'

    return return_val

	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        uploaded_file_name = 'uploadedImages/' + secure_filename(f.filename)
        f.save(uploaded_file_name)
        print('file uploaded at : ', uploaded_file_name)
        result = {
            "status": "file-uploaded-successfully",
            "uploadedImageServerRelativePath": uploaded_file_name
        }
        return json.dumps(result)
if __name__ == '__main__':
    print(__name__)
    app.run()
