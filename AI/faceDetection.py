import cv2 
import numpy as np
import threading
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
trackingRegister = (0,0,0,0)

cap = cv2.VideoCapture(0)


height = 720
width = 960
middle_x_frame = height/2
middle_y_frame = width/2

def followPerson(x,y,w,h) :
    for (x,y,w,h) in faces :
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 3)
            middle_x = (x + (x+w))/2
            middle_y = (y + (y+h))/2
            
            # offset between center and person
            offset_x = (middle_x - middle_x_frame)+ 40
            offset_y = (middle_y - middle_y_frame) + 240
            cv2.circle(frame, (int(middle_x), int(middle_y)),10, (255,0,0), 3)
            offset_z = w            
            cv2.putText(frame, "Followed Person", (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
           


while True :
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    height, width, channels = frame.shape
    
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) == 1 :
        for (x,y,w,h) in faces :    
            followedPerson = (x, y, w, h)
            trackingRegister = (x,y,w,h)
                
        for (x,y,w,h) in faces :
            followPerson(x,y,w,h)
            
    elif len(faces) == 0 :
        
        followedPerson = trackingRegister
        bordingBox = trackingRegister
        tracker.init(frame, bordingBox)

        success, bordingBox = tracker.update(frame)
    
        if success :
            x,y,w,h = int(bordingBox[0]),int(bordingBox[1]),int(bordingBox[2]),int(bordingBox[3])
            cv2.rectangle(frame, (x,y), ((x+w), (y+h)), (255,0,255), 3, 1)
            cv2.putText(frame, "Tracking", (75,75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)
        else :  
            cv2.putText(img, "Lost", (75,75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
    
    '''    
    else :
        followedPerson = (0, 0, 0, 0)
        
        for (x,y,w,h) in faces :
            if abs(w-x)> (followedPerson[2]-followedPerson[0]) :
                followedPerson =(x, y, w, h)
                trackingRegister =(x, y, w, h)
        faces = list(map(tuple,faces))
        
        
        if trackingRegister == (0,0,0,0) :
            followedPerson = trackingRegister
        Thread1 = threading.Thread(target=followPerson, args=(followedPerson[0], followedPerson[1], followedPerson[2], followedPerson[3]))
        Thread1.start()
        faces.remove((followedPerson[0], followedPerson[1], followedPerson[2], followedPerson[3]))
        for (x,y,w,h) in faces :
            
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 3)
            middle_x = (x + w)/2
            middle_y = (y + h)/2
            scale = w-x
            cv2.putText(frame, "NotFollowed Person", (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            
       '''     
    cv2.imshow('img', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()