import cv2 
import numpy as np
import threading
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
trackingRegister = (0,0,0,0)

cap = cv2.VideoCapture(0)



def followPerson(x,y,w,h) :
    for (x,y,w,h) in faces :
            
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 3)
            middle_x = (x + w)/2
            middle_y = (y + h)/2
            scale = w-x
            cv2.putText(frame, "Followed person Person", (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            if scale <= -50 :
                print("Move Forward")
            elif scale > -20 :
                print("Move back")
            else :
                print("Stable")
            if 200 <middle_x < 230 and 155 < middle_y < 185 :
                print("Stay STABLE")
            else :
                if 200 <= middle_x <= 230 :
                    print("")
                elif 230 < middle_x  :
                    print("Move right")
                else : 
                    print("Move left")
                
                if 155 <= middle_y <= 185 :
                    print("")
                elif middle_y < 185 :
                    print("Move down")
                else :
                    print("Move up")
            
   
   



while True :
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    height, width, channels = frame.shape

    # draw a line every 100 pixels
    for x in range(0, width -1, 160):
        cv2.line(frame, (x, 0), (x, height), (255, 0, 0), 1, 1)
    for y in range(0, height, 120):
        cv2.line(frame, (0,y), (width,y), (255,0,0), 1, 1)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
            
    if len(faces) == 1 :
        for (x,y,w,h) in faces :    
            followedPerson = (x, y, w, h)
                
        for (x,y,w,h) in faces :
                
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 3)
            middle_x = (x + w)/2
            middle_y = (y + h)/2
            scale = w-x
            cv2.putText(frame, "Followed Person", (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            if scale <= -50 :
                print("Move Forward")
            elif scale > -20 :
                print("Move back")
            else :
                print("Stable")
            if 200 <middle_x < 230 and 155 < middle_y < 185 :
                print("Stay STABLE")
            else :
                if 200 <= middle_x <= 230 :
                    print("")
                elif 230 < middle_x  :
                    print("Move right")
                else : 
                    print("Move left")
                
                if 155 <= middle_y <= 185 :
                    print("")
                elif middle_y < 185 :
                    print("Move down")
                else :
                    print("Move up")
    elif len(faces) == 0 :
        if trackingRegister == (0,0,0,0) :
            followedPerson = trackingRegister
        print(followedPerson)
        '''
        for (x,y,w,h) in followedPerson:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 3)
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
            
            
    cv2.imshow('img', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()