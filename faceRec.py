import cv2
import os
import sys
import numpy as np
import time
import smtplib
import re
import getpass
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from PIL import Image
from communicate import communicator

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
        people = [person for person in people if not person.endswith(".txt")]
    except:
        raise Exception("Must add a person to detect")

    faceCascade = cv2.CascadeClassifier("lbpcascade_frontalface.xml")
    rec = cv2.face.LBPHFaceRecognizer_create()
    threshold = 85
    images = []
    labels = []
    labels_people = {}
    for i, person in enumerate(people):
        labels_people[i] = person
        for image in os.listdir(people_folder + person):
            images.append(cv2.imread(people_folder + person + '\\' + image, 0))
            labels.append(i)
    try:
        rec.train(images, np.array(labels))
    except:
        raise Exception("OpenCV image training error")
        sys.exit()

    useEmail = True
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    getEmail = input("Enter gmail email: ")
    getPassword = getpass.getpass("Enter gmail Password: ")
    try:
        smtp_server.login(getEmail, getPassword)
    except:
        print("Email Failed -- Not Using Email")
        useEmail = False

    video = cv2.VideoCapture(0)
    video.set(3, 2000)
    video.set(4,2000)

    sender = communicator(True, None)
    people_found = set()
    last_rest = time.time()
    last_detect = time.time()
    last_count_reset = time.time()
    count = {person:0 for person in people}

    while True:
        if time.time() - last_count_reset > 5:
            last_count_reset = time.time()
            count = {person:0 for person in people}
        time.sleep(1/60)
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
                if time.time() - last_rest > 300:
                    people_found = set()
                    last_rest = time.time()
                if conf < threshold:
                    name = labels_people[pred].capitalize()
                    if name not in people_found and time.time() - last_detect > 5:
                        count[name] += 1
                        if count[name] < 30:
                            continue
                        last_detect = time.time()
                        people_found.add(name)
                        sender.sendMessage(name)
                    cv2.putText(frame, labels_people[pred].capitalize(),
                                (faces[i][0], faces[i][1] - 2),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1,
                                cv2.LINE_AA)
                else:
                    name = "Unknown"
                    if name not in people_found and len(people_found) >= 1:
                        people_found.add(name)
                        sender.sendMessage(name)
                        if useEmail:
                            cv2.imwrite("temp.jpg", frame)
                            msg = MIMEMultipart()
                            msg['Subject'] = 'Someone Unknown is at the Door!'
                            msg['From'] = getEmail
                            msg['To'] = getEmail
                            text = MIMEText("Here is a picture of who was at the door:")
                            msg.attach(text)
                            image = MIMEImage(open("temp.jpg", 'rb').read())
                            msg.attach(image)
                            smtp_server.sendmail(getEmail, getEmail, msg.as_string())
                            print("Email Sent")
                            os.remove("temp.jpg")
                    cv2.putText(frame, "Unknown",
                                (faces[i][0], faces[i][1]),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1,
                                cv2.LINE_AA)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            video.release()
            cv2.destroyAllWindows()
            smtp_server.quit()
            sys.exit()

recognize_people()
