import os
import cv2
import numpy as np
from PIL import Image

cascPath = "lbpcascade_frontalface.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataSet'

def preprocess():
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    for im in imagePaths:
        img = cv2.imread(im)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=7,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            sub_face = img[y:y+h, x:x+w]
            cv2.imwrite(im, sub_face)

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

for i in range(20):
    preprocess()
ids,faces = getImagesWithID(path)
recognizer.train(faces,np.array(ids))
recognizer.write('recognizer/trainingData.yml')
