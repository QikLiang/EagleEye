import cv2
import os
import sys
import numpy as np
import time
from PIL import Image

def modifyFrame(faces, frame, size=(100, 100)):
    images_rectangle = []
    for (x, y, w, h) in faces:
        images_rectangle.append(frame[y: y + h, x: x + w])

    images_norm = []
    for image in images_rectangle:
        is_color = len(image.shape) == 3
        if is_color:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        images_norm.append(cv2.equalizeHist(image))

    images_res = []
    for image in images_norm:
        is_color = len(image.shape) == 3
        if is_color:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if image.shape < size:
            image_res = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        else:
            image_res = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)
        images_res.append(image_res)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (206, 0, 209), 2)

    return frame, images_res

def recognize_people(people_folder = "people\\"):
    """ Start recognizing people in a live stream with your webcam
    """
    try:
        people = [person for person in os.listdir(people_folder)]
    except:
        raise Exception("Must add a person to detect")

    faceCascade = cv2.CascadeClassifier("lbpcascade_frontalface.xml")
    rec = cv2.face.LBPHFaceRecognizer_create()
    threshold = 80
    images = []
    labels = []
    labels_people = {}
    for i, person in enumerate(people):
        labels_people[i] = person
        for image in os.listdir(people_folder + person):
            images.append(cv2.imread(people_folder + person + '/' + image, 0))
            labels.append(i)
    try:
        rec.train(images, np.array(labels))
    except:
        raise Exception("OpenCV Error")
        sys.exit()

    video = cv2.VideoCapture(0)

    while True:
        time.sleep(1/30)
        if not video.isOpened():
            raise Exception('Unable to load camera.')

        # Capture frame-by-frame
        ret, frame = video.read()

        image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        scale_factor = 1.2
        min_neighbors = 5
        min_size = (30, 30)
        flags = cv2.CASCADE_SCALE_IMAGE
        faces = faceCascade.detectMultiScale(image_gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size, flags=flags)
        if len(faces):
            frame, faces_img = modifyFrame(faces, frame)
            for i, face_img in enumerate(faces_img):
                pred, conf = rec.predict(face_img)
                print ("Prediction: " + str(labels_people[pred].capitalize()), 'Confidence: ' + str(round(conf)))
                if conf < threshold:
                    cv2.putText(frame, labels_people[pred].capitalize(),
                                (faces[i][0], faces[i][1] - 2),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1,
                                cv2.LINE_AA)
                else:
                    cv2.putText(frame, "Unknown",
                                (faces[i][0], faces[i][1]),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1,
                                cv2.LINE_AA)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            video.release()
            cv2.destroyAllWindows()
            sys.exit()

recognize_people()
