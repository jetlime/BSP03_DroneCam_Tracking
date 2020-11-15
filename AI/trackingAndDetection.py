import cv2
import threading
import time
from functools import partial

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognisedFace = (0,0,0,0)
timing = True 
trackerCreated = False
checkLossMethodLaunched = False
cap = cv2.VideoCapture(0)



def isOverlapping(x1,y1,w1,h1,x2,y2,w2,h2) :
    if ((x1)<=x2<=(x1+w1) or x1<=(x2+w2)<=(w1+w1)) and (y1<=y2<=(y1+h2) or y1<=(y2+h2)<=(y1+h1)) :
        return True
    if (x2<=x1<=(x2+w2) or x2<=(x1+w1)<=(x2+w2)) and (y2<=y1<=(y2+h2) or y2<=(y1+h1)<=(y2+h2)) :
        return True
    return False

def drawBox(img, bbox) :
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img, (x,y), ((x+w), (y+h)), (255,0,255), 3, 1)
    cv2.putText(img, "Tracking", (75,75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)


def timingTracking() :
    time.sleep(1)
    global timing
    while True :
        if timing == False :
            timing = True 
            time.sleep(0.1)
        elif timing :   
            timing = False
            time.sleep(2)

def checkLoss(face) :
    checkLossMethodLaunched = True
    global bbox
    time.sleep(1)
    if face == bbox :
        print("Face lost")
        timing = True

    if face == (0,0,0,0) :
        print("facelost")
        timing = True

def pixelsToCm(x) :
    x = x/3
    if x < 20 :
        return 20
    elif x > 150 :
        return 150
    return int(x)

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

    height, width, _ = img.shape
    cv2.circle(img, (int(width/2),int(height/2)), 3, (255,0,0), 2)

    if timing :
        trackerCreated = False
        for (x,y,w,h) in faces :
            cv2.rectangle(img, (x,y), ((x+w), (y+h)), (255,255,255), 3, 1)
            cv2.putText(img, "Recognition", (175,75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)
            recognisedFace = (x,y,w,h)
        distance_x = abs(int(recognisedFace[0]+(recognisedFace[2]/2)) - int(width/2) )
        distance_y = abs(int(recognisedFace[1]+(recognisedFace[3]/2)) - int(height/2) )
        print(distance_x)
        cv2.circle(img, (int(recognisedFace[0]+(recognisedFace[2]/2)),int(recognisedFace[1]+(recognisedFace[3]/2))), 3, (255,0,0), 2)
        
    else : 
        if "success" in globals() :
            drawBox(img, bbox)
            if not(checkLossMethodLaunched) :
                checkLossWithArg = partial(checkLoss, bbox)
                checkLossThread = threading.Thread(target=checkLossWithArg)
                checkLossThread.start()
            distance_x = abs(int(bbox[0]+(bbox[2]/2)) - int(width/2) )
            distance_y = abs(int(bbox[1]+(bbox[3]/2)) - int(height/2) )
            print("move " + str(pixelsToCm(distance_x)) + " cm")
            cv2.circle(img, (int(bbox[0]+(bbox[2]/2)),int(bbox[1]+(bbox[3]/2))), 3, (255,0,0), 2)
        else :  
            cv2.putText(img, "Lost", (75,75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)

    cv2.imshow("Tracking", img)

    if cv2.waitKey(1) & 0xff == ord('q') :
        break