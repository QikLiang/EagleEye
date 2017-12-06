import os
import cv2
import numpy as np
from PIL import Image

cascPath = "lbpcascade_frontalface.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataSet'

def preprocess():
    count = 0
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    for im in imagePaths:
        print("Processing: " + str(im))
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
            cv2.imwrite(str(im[:-4]) + "." + str(count) + ".jpg", sub_face)
            count += 1
        os.remove(im)


def resize(size=(100, 100)):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    for im in imagePaths:
        print("Resizing: " + str(im))
        img = cv2.imread(im)
        if img.shape == size:
            continue
        if img.shape < size:
            image_norm = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
        else:
            image_norm = cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(im, image_norm)

resize()
# preprocess()
