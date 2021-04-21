import cv2
import numpy as np
from PIL import Image
import sqlite3

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.EigenFaceRecognizer_create()

recognizer.read('recognizer/trainingData.yml')
#give data from SQLite follow ID
def getProfile(id):
    conn = sqlite3.connect('dataFromCam.db')
    query = "Select * from People Where ID= " + str(id)
    cursor = conn.execute(query)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile

#making text font
fontface = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)
while(True):
    #camera action
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray)
    for (x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        id, configparser = recognizer.predict(roi_gray)
        if configparser < 40:
            profile = getProfile(id)
            #load info to camera
            if (profile != None):
                cv2.putText(frame, "Name: " + str(profile[1]), (x + 10, y + h + 30), fontFace, 1, (0, 255, 0), 2)
                cv2.putText(frame, "Age: " + str(profile[2]), (x + 10, y + h + 60), fontFace, 1, (0, 255, 0), 2)
                cv2.putText(frame, "Gender: " + str(profile[3]), (x + 10, y + h + 90), fontFace, 1, (0, 255, 0), 2)
        else:
            cv2.putText((frame, "Unknow", (x + 10, y + h + 90), fontFace, 1, (0, 255, 0), 2))
    cv2.imshow('Image', frame)
    if (cv2.waitKey(100) & 0xFF == ord('q')):
            break
cap.release()
cv2.destroyAllWindows()