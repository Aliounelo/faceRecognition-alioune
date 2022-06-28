"""
Haar Cascade Face detection with OpenCV  
    Based on tutorial by superdatascience.com && docs.opencv.org
    Visit original posts: https://www.superdatascience.com/blogs/opencv-face-recognition, https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html
Adapted by Alioune LO - Z01D3R @ 7Jun2022 

"""

import cv2
import time



#-- Detect and display Face
def detectFaces(cascade, img_copy, scaleFactor=1.027) :
    
    img_copy = img.copy()
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    #-- Detect Faces
    faces = cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5)
    for (x,y,w,h) in faces : 
        cv2.rectangle(img_copy, (x,y), (x+w, y+h), (255, 0, 0), 2)

    #-- Display Faces
    cv2.imshow('Capture - Face Detection', img_copy)    
    print("Faces found :", len(faces))

haar_cascade =  cv2.CascadeClassifier('../opencv-3.4/data/haarcascades/haarcascade_frontalface_alt.xml')
lbp_cascade = cv2.CascadeClassifier('../opencv-3.4/data/lbpcascades/lbpcascade_frontalface.xml')
img = cv2.imread('../images/multiFace.jpeg')

#-- Time execution for LBP cascade
ta = time.time()
detectFaces(lbp_cascade,img)
tb = time.time()
dt = tb- ta
print(dt)


#-- Time execution for Haar Cascade 
t1 = time.time()
detectFaces(haar_cascade,img)
t2 = time.time()
dt1 = t2 - t1
print(dt1) 


cv2.waitKey(0)
cv2.destroyAllWindows()