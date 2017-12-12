import os
import cv2

file_separater = '/'

cascPath = "lbpcascade_frontalface.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
size=(100, 100)
person = input("What is the persons name: ")
person = person.lower()
if not os.path.exists('people/' + person + '/'):
    os.makedirs('people/' + person + '/')

counter = 0
for fi in os.listdir('process'):
    if ".jpg" not in str(fi) and ".png" not in str(fi):
        continue
    img = cv2.imread('process/' + fi)
    image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    scale_factor = 1.2
    min_neighbors = 5
    min_size = (30, 30)
    flags = cv2.CASCADE_SCALE_IMAGE
    face_coord = faceCascade.detectMultiScale(image_gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size, flags=flags)

    if len(face_coord):
        images_rectangle = []
        for (x, y, w, h) in face_coord:
            images_rectangle.append(img[y: y + h, x: x + w])

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
            # using different OpenCV method if enlarging or shrinking
            if image.shape < size:
                image_res = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
            else:
                image_res = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)
            images_res.append(image_res)

            while os.path.exists('people/' + person + '/' + str(counter) + '.jpg'):
                counter += 1

            cv2.imwrite('people/' + person + '/' + str(counter) + '.jpg', images_res[0])
            counter += 1
    os.remove("process/" + fi)
