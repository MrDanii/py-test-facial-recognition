import os
import sys
from PIL import Image
from flask import Flask, jsonify, request
import face_recognition
import face_recognition_models

# trying to import this shit but I dont know python
from databaseconf.connect import connect as testConnect
from databaseconf.config_db import load_config

# Database services imports
from databaseconf.services_facial_recognition import insertEmbedding

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))
myDbConfig = load_config()

# * Healtch Check Method, for API and database
@app.route('/user/<username>/<int:user_id>', methods=['POST'])
def showUserProfile(username, user_id):
    # show the user profile for that user
    testConnect(myDbConfig)
    return {
        "id": user_id,
        "user": username,
    }
    # return f'User: {username} \t Id: {user_id}'


# * Method that receives an image and returns his face embeddings; returns Float[]
@app.route('/facial-recognition/process-image', methods=['POST'])
def generateImageEmbeddings():
    if 'image' not in request.files:
        return jsonify({
            "error": "No image file provided",
            "message": "No image file provided",
            "status": 400
        }), 400

    file = request.files['image']
    # image = Image.open(file.stream)

    print('File >>>>', file=sys.stderr)
    print(file.name, file=sys.stderr)
    # print('Image >>>>', file=sys.stderr)
    # print(image, file=sys.stderr)

    imageLoaded = face_recognition.load_image_file(file)
    imageEncodingsArray = face_recognition.face_encodings(imageLoaded)[0]

    # print(imageAnalized, file=sys.stderr)
    print("Encoding >>>>", imageEncodingsArray.itemsize, file=sys.stderr)
    print("Encoding >>>>", imageEncodingsArray.size, file=sys.stderr)   # 128 array size
    print(imageEncodingsArray, file=sys.stderr)
    
    idAddressPersonImage = insertEmbedding([.1, .02, .003, .00004])
    print(idAddressPersonImage, file=sys.stderr)

    # Aquí podrías procesar la imagen, como extraer el embedding, etc.
    # Por ejemplo, vamos a simular un resultado de procesamiento.
    result = {
        "message": "Image processed successfully",
        "status": 200,
        # "ebeddigns": jsonify(imageEncoding)
    }

    return jsonify(result)

# * Method that receives an image and compares all image embeddings stored in Database
@app.route('/facial-recognition/compare-image', methods=['POST'])
def compareImageByAddress():
    if 'image' not in request.files:
        return jsonify({
            "error": "No image file provided",
            "message": "No image file provided",
            "status": 400
        }), 400

    file = request.files['image']
    image = Image.open(file.stream)

    result = {
        "message": "Image processed succesfully",
        "status": 200
    }
    return jsonify(result)
