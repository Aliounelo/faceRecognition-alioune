"""
    Classifier : OpenCV Haar Cascade for face detection
    Recognizer : OpenCV LPBH Face recognizer
    Based on tutorial by superdatascience.com && docs.opencv.org && towardsdatascience.com && code.luasoftware.com
    Visit original posts: https://www.superdatascience.com/blogs/opencv-face-recognition, https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html, https://www.thepythoncode.com/article/get-hardware-system-information-python#Network_info
                          https://towardsdatascience.com/real-time-face-recognition-an-end-to-end-project-b738bb0f7348, https://code.luasoftware.com/tutorials/telegram/telegram-send-photo-to-channel/
    APIs : https://app.abstractapi.com/api/ip-geolocation/tester, https://core.telegram.org/api

Adapted by Alioune LO - Z01D3R @ 16Jun2022 

"""

import os
import cv2
import time
from dbus import NameExistsException
import requests
import platform
#import datetime
import telegram
import numpy as np
from PIL import Image

#-- Telegram bot token and group chat ID to set up alert messages
token = '5535933470:AAFWP__W6-1fAxqrCQbE2QTXFDygnZhFnN8'
chatID = '-696427975'


#-- Train faces detected using the 01-samples.py script
path = "training-data"
recognizer = cv2.face.LBPHFaceRecognizer_create() 
detector = cv2.CascadeClassifier('../opencv-3.4/data/haarcascades/haarcascade_frontalface_alt.xml')
bot = telegram.Bot(token=token)

imagePaths = []
faceSamples=[]
ids = []

namesAndIds = {}

#-- API for geolocation and more informations about the users 
response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=926c0917bf5e42fda8e40569e5c796fb")
uname = platform.uname()

global username, isAccessing

def alertMessage(alert,username,id) :
    print("[WARNING] Access GRANTED !")
    message =  "{\n" + "="*3 + "User Informations" + "="*3 + f"\nUsername : {username}\nID:{id}\nSystem: {uname.system}\nNode Name: {uname.node}\nRelease: {uname.release}\nVersion: {uname.version}\nMachine: {uname.machine}\n" + f"{response.status_code}\n" +"="*3 + "More" + "="*3 + f"\n{str(response.content)}" +"\n}"
    bot.send_photo(chat_id=chatID, photo=open(f"/tmp/{username}.jpg", 'rb'))
    bot.send_message(chat_id=chatID, text=message)

    #-- Go through the image samples directory and get the absolute paths
for f in os.listdir(path) :
    imageDirectories = os.path.join(path,f)
    print(imageDirectories)
    dir = os.listdir(imageDirectories)
    for samples in dir :
        print(f"    |- - - - {samples}-> id:{f}")
    imagePaths.append(os.path.join(imageDirectories,samples))
    

    #-- Get the ids and face samples, put them into arrays 
for imagePath in imagePaths:
    PIL_img = Image.open(imagePath).convert('L') # grayscale
    img_numpy = np.array(PIL_img,'uint8')
    names = os.path.split(imagePath)[-1].split("-")[0]
    id = int(os.path.split(imagePath)[-2].split("/")[1])
    
    namesAndIds.update({id:names})

    faces = detector.detectMultiScale(img_numpy)
    for (x,y,w,h) in faces:
        faceSamples.append(img_numpy[y:y+h,x:x+w])
        ids.append(id)

    #-- Save the model into trainer/trainer.yml       
recognizer.train(faceSamples, np.array(ids))

print("\n",namesAndIds)

    #-- Print the numer of faces trained and end program
recognizer.write('./training-data.yml') 
print("\n [INFO] {0} face(s) trained. Do you want to continue ?\n".format(len(np.unique(ids))))

font = cv2.FONT_HERSHEY_SIMPLEX
#-- indicate the id counter
id = 0 

#-- Face recognition step
answer = input("1-YES\n2-NO\n>>")
if answer in ["2","NO","no"] :
    exit(0)

elif answer in ["1","yes","YES"] :  
    recognizer.read('training-data.yml')
        #-- Read the video stream
    cap = cv2.VideoCapture(3)
    cap.set(3,640) #-- set Width
    cap.set(4,480) #-- set Height
    #-- Define min window size to be recognized as a face
    minW = 0.1*cap.get(3)
    minH = 0.1*cap.get(4)

    t1 = time.time()
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
        faces = detector.detectMultiScale( 
            gray,
            scaleFactor = 1.025,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        
            #-- If confidence is less than 100 ==> "0" : perfect match | confidence doesn't represent decision rate but the distance used by the LPBH
        if (confidence < 100):
            username = namesAndIds[id]
            confidence = "  {0}%".format(round(100 - confidence))
            isAccessing = True

        else:
            username = "searching"
            confidence = "  {0}%".format(round(100 - confidence))
            isAccessing = False
        
        cv2.putText(
                    img, 
                    str(username), 
                    (x+5,y-5), 
                    font, 
                    1, 
                    (255,255,255), 
                    2
                   )
        cv2.imwrite(f"/tmp/{username}.jpg",gray[y:y+h,x:x+w])

        #-- Press 'ESC' for exiting video or wait 10s for automated exit 
        #k = cv2.waitKey(10) & 0xff 
        #if k == 27:
        break

################### -- Make a try to verify the connectivity before using the Telegram API   
    try :
        t2 = time.time()
        if isAccessing == True : 
            alertMessage("SOMEONE ACCESSED YOUR SYSTEM",username,id)
            os.remove(f"/tmp/{username}.jpg")
        else :
            print("[WARNING] Access DENIED !")
            bot.send_photo(chat_id=chatID, photo=open(f"/tmp/{username}.jpg", 'rb'))
            bot.send_message(chat_id=chatID, text="SOMEONE IS TRYING TO ACCESS YOUR SYSTEM")
            os.remove(f"/tmp/{username}.jpg")
    except NameError as e :
        print("[WARNING] Make sure your internet connection is working",e)

    dt = t2 - t1
    print("[INFO] Facial recognition executing time : {0}".format(dt))
else :
    print("--(!) Error unavalaible choice")
    exit(0)


#cv2.imshow('camera',img) 