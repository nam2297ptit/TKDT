import cv2,os
import math
import argparse
import config
def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn=frame.copy()
    frameHeight=frameOpencvDnn.shape[0]
    frameWidth=frameOpencvDnn.shape[1]
    blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections=net.forward()
    faceBoxes=[]
    for i in range(detections.shape[2]):
        confidence=detections[0,0,i,2]
        if confidence>conf_threshold:
            x1=int(detections[0,0,i,3]*frameWidth)
            y1=int(detections[0,0,i,4]*frameHeight)
            x2=int(detections[0,0,i,5]*frameWidth)
            y2=int(detections[0,0,i,6]*frameHeight)
            faceBoxes.append([x1,y1,x2,y2])
            cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn,faceBoxes


parser=argparse.ArgumentParser()
parser.add_argument('--image')

args=parser.parse_args()

faceProto="library/opencv_face_detector.pbtxt"
faceModel="library/opencv_face_detector_uint8.pb"
ageProto="library/age_deploy.prototxt"
ageModel="library/age_net.caffemodel"
genderProto="library/gender_deploy.prototxt"
genderModel="library/gender_net.caffemodel"

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(20-30)', '(30-40)', '(48-53)', '(60-100)']
genderList=['Male','Female']

faceNet=cv2.dnn.readNet(faceModel,faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)

video=cv2.VideoCapture(args.image if args.image else 0)
if (video.isOpened() == False ): video=cv2.VideoCapture(2)
padding=20
count =0
while cv2.waitKey(1)<0:
    hasFrame,frame=video.read()
    if not hasFrame:
        cv2.waitKey()
        break

    resultImg,faceBoxes=highlightFace(faceNet,frame)
    if not faceBoxes:
        print("No face detected")

    if len(faceBoxes) > 0:
        faceBoxes = sorted(faceBoxes, reverse=True)[-1]
        face=frame[max(0,faceBoxes[1]-padding):
                   min(faceBoxes[3]+padding,frame.shape[0]-1),max(0,faceBoxes[0]-padding)
                   :min(faceBoxes[2]+padding, frame.shape[1]-1)]

        blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds=genderNet.forward()
        gender=genderList[genderPreds[0].argmax()]
        #print(f'Gender: {gender}')

        ageNet.setInput(blob)
        agePreds=ageNet.forward()
        age=ageList[agePreds[0].argmax()]
        #print(f'Age: {age[1:-1]} years')

        cv2.putText(resultImg, f'{gender}, {age}', (faceBoxes[0], faceBoxes[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2,cv2.LINE_AA)	        	
        cv2.imshow("Detecting age and gender", resultImg)
        count += 1
        if(count == 50):
           cmd =  "mosquitto_pub -h " + config.server + " -t " + config.topic + " -m " + gender + "," + age[1:-1]  + " -u " + config.username + " -P " + config.password + " -p "  + str(config.port)
           #print(cmd)
           #os.system(cmd)
           #cv2.destroyAllWindows()
           #exit(0)

