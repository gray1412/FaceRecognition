import cv2
import sqlite3
import os

#Insert or Update dataset
def insertORUpdate(id, name, age, gender):
    conn = sqlite3.connect('dataFromCam.db')

    query = "Select * from People Where ID= " + str(id)

    cursor = conn.execute(query)

    isREcordExist = 0

    for row in cursor:
        isREcordExist = 1

    if(isREcordExist == 0):
        query = "Insert into People(ID, Name, Age, Gender) values(" + str(id) + ",'" + str(name) + "','" + str(age) + "','" + str(gender) + "')"
    else:
        query = "Update People set Name = '" + str(name) + "', Age = '" + str(age) + "', Gender = '" + str(gender) + "' Where ID = " +str(id)

    conn.execute(query)
    conn.commit()
    conn.close()
#insert to database
id = input("Enter your ID: ")
name = input("Enter your Name: ")
age = input("Enter your Age: ")
gender = input("Enter your Gender: ")
insertORUpdate(id, name, age, gender)

#load
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)
sampleNum = 0

while(True):
    #camera action
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if not os.path.exists('dataSet'):
        os.makedirs('dataSet')
    sampleNum += 1

    for (x, y, w, h) in faces:
        cv2.imwrite("dataSet/User."+id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h, x:x+w]) #gray[y:y+h, x:x+w]

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    #limit 200 image
    if sampleNum > 200:
        break

cap.release()
cv2.destroyAllWindows()