"""
Haar Cascade Face detection with OpenCV  
    Based on tutorial by superdatascience.com && docs.opencv.org
    Visit original posts: https://www.superdatascience.com/blogs/opencv-face-recognition, https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html
Adapted by Alioune LO - Z01D3R @ 7Jun2022 

"""

import cv2
import os
import time


haar_cascade =  cv2.CascadeClassifier('../opencv-3.4/data/haarcascades/haarcascade_frontalface_alt.xml')


#-- userID as directory name and username as img name.
id = input("Numero de matricule : ")
user=input("Nom d'utilisateur : ")

if os.path.exists("training-data") :
    try :
        os.mkdir(f"training-data/{id}")
    except FileExistsError as err : 
        print(err)

#-- Read the video stream
cap = cv2.VideoCapture(3)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0) 

count=0
while True:

    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #-- Detect Faces
    faces = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minSize=(30,30), minNeighbors=5)
    
    for (x,y,w,h) in faces : 
    
        frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)

        #-- Save images
        cv2.imwrite(f"training-data/{id}/{user}" +  '-' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        count += 1

        #-- Display Faces
        #cv2.imshow('Capture - Face Detection', frame)    
   
    k = cv2.waitKey(100) & 0xff 
    if k == 27:
        break
    elif count >= 100: 
        break

print("[INFO] Done taking samples.")
cap.release()
cv2.destroyAllWindows()







