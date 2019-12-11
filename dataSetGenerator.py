import sys
sys.path.insert(0,'person')

import cv2
from person import *

new_name = None
while True:
    new_name = str(input("Enter your name: ")).lower()
    if person.append_data(new_name):
        break

new_id = person.person[0]["nums"]

print ("Start generator sample photo!")
print ("Please look at the camera until the stop message appears!")

try:
    cam = cv2.VideoCapture(0)
    detector=cv2.CascadeClassifier('Classifiers/face.xml')
    i = 0

      
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.25, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            #incrementing sample number 
            i += 1
            cv2.imwrite("dataSet/face-"+ str(new_id) +'.'+ str(i) + ".jpg", gray[y:y+h,x:x+w])
            print(i,end = "")
            print("%")
        cv2.imshow('frame',img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        elif i>=100:
            print ("OK")
            break
    cam.release()
    cv2.destroyAllWindows()
except:
    print ("Error")
    person.pop_data()
    cam.release()
    cv2.destroyAllWindows()

