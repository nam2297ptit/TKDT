import sys
sys.path.insert(0,'person')

from person import *
import cv2,os
import numpy as np
from PIL import Image 
import pickle
import time
import config

recognizer=cv2.face.LBPHFaceRecognizer_create();
recognizer.read('trainer/trainer.yml')
cascadePath = "Classifiers/face.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
path = 'dataSet'

cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_TRIPLEX

last_time = time.time()

count = list(range(0, person.person[0]["nums"]+1))

for i in range(0, person.person[0]["nums"]+1):
    count[i] = 0


print ("Please look at the camera until the stop message appears!")

while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, scaleFactor=1.25, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    
    for(x,y,w,h) in faces:
        nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
        
        if conf < 45:
            count[nbr_predicted] += 1
            nbr_predicted=person.person[nbr_predicted]["name"]
            cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(0,255,0),2)
            cv2.putText(im,str(nbr_predicted)+" - "+str("{0}%".format(round(100-conf))), (x-25,y+h),font,2 , (0,255,0)) #Draw the text
        else:
            count[0] += 1
            nbr_predicted = "Unknown"
            cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(0,0,255),2)
            cv2.putText(im,str(nbr_predicted), (x-25,y+h+40),font,1 ,(0,0,255)) #Draw the text
            
        #phan gui du lieu len  
        for i in range(0, person.person[0]["nums"]+1):
            
          if count[i]> 50:
              if i==0:
                  unknown = "unknown"
                  print (unknown)
                  cmd =  "mosquitto_pub -h " + config.server + " -t " + config.topic + " -m " + unknown + " -u " + config.username + " -P " + config.password + " -p "  + str(config.port) 
              else:
                  name = person.person[i]["name"]
                  print (name)
                  #cmd =  "mosquitto_pub -h " + config.server + " -t " + config.topic + " -m ok -u " + config.username + " -P " + config.password + " -p "  + str(config.port) 
              #print(cmd)
              #os.system(cmd)
              #cam.release()
              #cv2.destroyAllWindows()
              #exit(0)

    cv2.imshow('im',im)
       
    if cv2.waitKey(1)&0xFF == ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        exit(0)
