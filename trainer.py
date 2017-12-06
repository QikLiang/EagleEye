import os
import cv2
import numpy as np
from PIL import Image

cascPath = "lbpcascade_frontalface.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataSet'

def getImagesWithID(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    facesList = []
    ids = []
    for im in imagePaths:
        imageID = int(os.path.split(im)[-1].split('.')[1])
        faceImg=Image.open(im).convert('L')
        faceNp=np.array(faceImg, 'uint8')
        facesList.append(faceNp)
        ids.append(imageID)
    return ids, facesList

ids,faces = getImagesWithID(path)
recognizer.train(faces,np.array(ids))
recognizer.write('recognizer/trainingData.yml')
