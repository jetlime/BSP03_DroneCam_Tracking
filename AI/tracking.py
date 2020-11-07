import cv2
import threading
import time
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognisedFace = (0,0,0,0)
timing = True 
trackerCreated = False
cap = cv2.VideoCapture(0)


def drawBox(img, bbox) :
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img, (x,y), ((x+w), (y+h)), (255,0,255), 3, 1)
    cv2.putText(img, "Tracking", (75,75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)


def timingTracking() :
    time.sleep(2)
    global timing
    while True :
        if timing == False :
            timing = True 
            time.sleep(1)
        elif timing :   
            timing = False
            time.sleep(5)

timeThread = threading.Thread(target=timingTracking)
timeThread.start()
while True :
    _ , img = cap.read()
    if timing == False :
        if trackerCreated == False :
            tracker = cv2.TrackerMOSSE_create()
            success, img = cap.read()
            bbox = recognisedFace
            tracker.init(img, bbox)
            trackerCreated = True 
            print(bbox)

    if trackerCreated :
        success, bbox = tracker.update(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if timing :
        trackerCreated = False
        for (x,y,w,h) in faces :
            cv2.rectangle(img, (x,y), ((x+w), (y+h)), (255,255,255), 3, 1)
            cv2.putText(img, "Recognition", (175,75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)
        recognisedFace = (x,y,w,h)
        
    else : 
        if "success" in globals() :
            drawBox(img, bbox)
        else :  
            cv2.putText(img, "Lost", (75,75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)

    cv2.imshow("Tracking", img)

    if cv2.waitKey(1) & 0xff == ord('q') :
        break