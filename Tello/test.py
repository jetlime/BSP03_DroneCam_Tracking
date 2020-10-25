from djitellopy import Tello
import cv2
import time 

width = 320
height = 240
startCounter = 1
middle_x_frame = height/2
middle_y_frame = width/2
me = Tello()
me.connect()
me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

me.streamoff()
me.streamon()

while True :
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if startCounter == 0 :
        me.takeoff()
        
        startCounter = 1
    
    for (x,y,w,h) in faces :

            # middle of person
            middle_x = (x + (w/2))
            middle_y = (y + (h/2))
            # offset between center and person
            offset_x = (middle_x - middle_x_frame)
            offset_y = (middle_y - middle_y_frame)
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 1, 1)
            offset_z = w
            
            if middle_x < int(middle_x_frame- 30) :
                print("Go left")
                dir = 1
            elif middle_x > int(middle_x_frame + 30) :
                print("Go right")
                dir = 2
            elif middle_y < int(middle_y_frame - 30) :
                print("Go up")
                dir = 3 
            elif middle_y > int(middle_y_frame + 30) :
                print("Go Down")
                dir = 4
            else :
                dir = 0
                '''
            if offset_x > 10 :
                me.move_right(20)
            elif offset_x < -10 :
                me.move_left(20)
        '''
    if dir == 1 : 
        me.yaw_velocity = - 60
    elif dir == 2 :
        me.yaw_velocity = -60
    elif dir == 3 : 
        me.up_down_velocity = -60
    elif dir == 4 :
        me.left_right_velocity = 0; me.for_back_velocity = 0; me.up_down_velocity = 0; me.yaw_velocity = 0
        
    if me.send_rc_control :
        me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        me.land()
        break