"""
Haar Cascade Face detection with OpenCV  
    Based on tutorial by superdatascience.com && docs.opencv.org
    Visit original posts: https://www.superdatascience.com/blogs/opencv-face-recognition, https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html
Adapted by Alioune LO - Z01D3R @ 7Jun2022 

"""

import cv2
import time

#-- 1. Detect and display Face
def detectFaces(cascade, frame, scaleFactor=1.1): 
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #-- Detect Faces
    faces = cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5)
    for (x,y,w,h) in faces : 
        frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)

    #-- Display Faces
    cv2.imshow('Capture - Face Detection', frame)    
    print("Faces found :", len(faces))

haar_cascade =  cv2.CascadeClassifier('../opencv-3.4/data/haarcascades/haarcascade_frontalface_alt.xml')
lbp_cascade = cv2.CascadeClassifier('../opencv-3.4/data/lbpcascades/lbpcascade_frontalface.xml')

#-- 2. Read the video stream
cap = cv2.VideoCapture(4)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

if not cap.isOpened:
    print('--(!) Error opening video capture')
    exit(0)


while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    t1 = time.time()
    detectFaces(haar_cascade,frame)
    t2 = time.time()

    dt1 = t2 - t1
    print(dt1) 
    if cv2.waitKey(10) == 27 :
        break







