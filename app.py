import os
import sys
from PIL import Image
from flask import Flask, jsonify, request
import face_recognition
import face_recognition_models
import numpy

# trying to import this shit but I dont know python
from databaseconf.connect import connect as testConnect
from databaseconf.config_db import load_config

# Database services imports
from databaseconf.services_facial_recognition import insertEmbedding
from databaseconf.services_facial_recognition import getAllPersonImages

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

    # Get Image from request
    file = request.files['image']

    # Getting vectors from image file
    imageLoaded = face_recognition.load_image_file(file)
    imageEncodingsVector = face_recognition.face_encodings(imageLoaded)[0]

    # print("Encoding >>>>", imageEncodingsArray.itemsize, file=sys.stderr)
    # print("Encoding >>>>", imageEncodingsArray.size, file=sys.stderr)   # 128 array size
    # print(imageEncodingsArray, file=sys.stderr)

    # In case we need to insert in DB
    # insertEmbedding(imageEncodingsArray.tolist())
    
    result = {
        "message": "Image processed successfully",
        "status": 200,
        "embeddings": imageEncodingsVector.tolist()
        # "embeddings": jsonify(imageEncodingsArray.tolist())
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

    # Get image from request
    file = request.files['image']

    # Getting vectors from image file
    imageLoaded = face_recognition.load_image_file(file)
    imageLoadedEncodingsVector = face_recognition.face_encodings(imageLoaded)[0]
    
    # Getting all vector from database
    imagesEncodingsPersonsArray = getAllPersonImages()
    # variable to store our vectors, this will be an array of vectors
    encodingsPersonsVector = []
    for encodingPerson in imagesEncodingsPersonsArray:
        encodingsPersonsVector.append(numpy.array(encodingPerson[2]))
    
    # compare all images against our image provided, this returns an array of vectors with booleans (true for matches in databases)
    vectorsResult = face_recognition.compare_faces(encodingsPersonsVector, imageLoadedEncodingsVector)
    print(vectorsResult, file=sys.stderr)

    firstMatchIndex = numpy.argmax(vectorsResult)   # give us the index of firstmatch
    if vectorsResult[firstMatchIndex] == True :
        print(firstMatchIndex, file=sys.stderr)
        idAddressPersonFound = imagesEncodingsPersonsArray[firstMatchIndex][0]
        personName = imagesEncodingsPersonsArray[firstMatchIndex][1]
        print("idAddressPersonFound: " + str(idAddressPersonFound), file=sys.stderr)
        result = {
            "message": "Image processed succesfully. User Found",
            "status": 200,
            "idAddressPersonName": idAddressPersonFound,
            "personName": personName
        }
    else :
        print("User Face not registered", file=sys.stderr)
        result = {
            "message": "Image processed succesfully, User NOT Found",
            "status": 404,
            "idAddressPersonName": None,
            "personName": None
        }

    return jsonify(result)
