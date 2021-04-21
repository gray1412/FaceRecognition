import cv2
import numpy as np
import os
from PIL import Image

recognizer = cv2.face.EigenFaceRecognizer_create()
path = 'dataSet'

def getImagesWitdthID(path):
    #give image's link
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    print(imagePaths)

    faces = []
    IDs = []

    for imagePaths in imagePaths:
        faceImg = Image.open(imagePaths).convert('L')
        faceNp = np.array(faceImg,'uint8')
        print(faceNp)
        #cut to give image's ID
        ID = int(imagePaths.split('\\')[1].split('.')[1])

        faces.append(faceNp)
        IDs.append(ID)

        cv2.imshow('Trainning', faceNp)
        cv2.waitKey(5000)

        return faces, IDs
faces, IDs = getImagesWitdthID(path)

#training
recognizer.train(faces, np.array(IDs))

#saving
if not os.path.exists('recognizer'):
    os.makedirs('recognizer')

recognizer.save('recognizer/trainingData.yml')

cv2.destroyAllWindows()


