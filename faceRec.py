import cv2
import os
import numpy as np
import time
from PIL import Image

rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer/trainingData.yml")
path = 'dataSet'

cascPath = "lbpcascade_frontalface.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

def resize(img, size=(100, 100)):
    if img.shape < size:
        image_norm = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    else:
        image_norm = cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)
    return image_norm

def detectFace(faces, img):
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        faceImg=Image.fromarray(img).convert('L')
        faceNp=np.array(faceImg, 'uint8')
        label, conf = rec.predict(resize(faceNp))
        print(label, conf)
        if conf < 140:
            if label == 1:
                name = "Matthew"
            elif label == 2:
                name = "Christian"
            elif label == 3:
                name = "Qi"
            else:
                name = "Unknown"
        else:
            name = "Unknown"

        cv2.putText(img, str(name), (x, y + h), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

def convertToRGB(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

video_capture = cv2.VideoCapture(0)

while True:
    time.sleep(1/30)
    if not video_capture.isOpened():
        raise Exception('Unable to load camera.')

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    detectFace(faces, frame)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Display the resulting frame
cv2.imshow('Video', frame)  # When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
