import time
import cv2
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import threading
import socket
import sys
import platform  
from functools import partial
from djitellopy import Tello

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

videoRecording = False
followmode = False 
me = Tello()
me.connect()
me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0

dir = 0 

me.streamoff()
me.streamon()

root= tk.Tk()
root.geometry('1366x768')
frame = tk.Frame(root, relief=tk.RIDGE, borderwidth=2)
frame.pack(fill=tk.BOTH,expand=1)
root.title('Tello Drone')
frame.config(background='light blue')
s = ttk.Style()
s.theme_use('clam')
s.configure("TProgressbar", foreground='red', background='red')

def labelling() :
    while True :
        batteryLevel = int(me.get_battery())
        if batteryLevel > 50 :
            s.configure("TProgressbar", foreground='red', background='green')
        elif batteryLevel > 20 and batteryLevel <= 50 :
            s.configure("TProgressbar", foreground='red', background='orange')
        else :
            s.configure("TProgressbar", foreground='red', background='red')

        if me.get_wifi() :
            label4 = tk.Label(frame, text = 'Drone connected' , width = '90', font=("Courier", 18), bg = "green")
            label1 = tk.Label(frame, text = 'Battery level : ' + str(batteryLevel) + "%", width = '90', font=("Courier", 18))
            progressbar1 = ttk.Progressbar(frame, style = "TProgressbar", orient = tk.HORIZONTAL, length = 600, mode = 'determinate', value = str(batteryLevel))
            label2 = tk.Label(frame, text = 'Height :' + str(me.get_height()), width = '90', font=("Courier", 18))
            label3 = tk.Label(frame, text = 'Flight Time :' + str(me.get_flight_time()), width = '90', font=("Courier", 18))
            progressbar1.place(x = 350, y = 68)
        else :
            label4 = tk.Label(frame, text = 'Drone not connected' , width = '90', font=("Courier", 18), bg = "red")
            label1 = tk.Label(frame, text = 'Battery level : connect drone to see information ', width = '90', font=("Courier", 18))
            label5 = tk.Label(frame, text = ' ', width = '90', font=("Courier", 18))
            label2 = tk.Label(frame, text = 'Height : connect drone to see information', width = '90', font=("Courier", 18))
            label3 = tk.Label(frame, text = 'Flight Time : connect drone to see information', width = '90', font=("Courier", 18))        
            label5.place(x = 30, y = 60)

        label1.place(x = 30, y = 30)
        label2.place(x = 30, y = 90)
        label3.place(x = 30, y = 120)
        label4.place(x = 30, y = 0)
        time.sleep(5)

labellingThread = threading.Thread(target= labelling)
labellingThread.start()

def stream() :
    streambeginThread = threading.Thread(target=streamBegin)
    streambeginThread.start()
    
def exitt() :
    me.streamoff()
    exit()
    

def takeoff() :
    me.takeoff()

def up(y) : 
    me.move_up(y)

def land() : 
    me.land()

def right(x) : 
    me.move_right(x)

def down(y) :
    me.move_down()

def left(x) : 
    me.move_left(x)

def forward(z) :
    me.move_forward(z)

def back(z) :
    me.move_back(z)

def rotate(x) : 
    me.rotate_clockwise(x)


def counterRotate(x) :
    me.rotate_counter_clockwise(x)

def react(a,b,c,d) :
    me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)

def followMode() :
    global followmode
    if followmode :
        followmode = False
    elif followmode == False :
        followmode = True

def updateFollowMode() :
    while True :
        if followmode : 
            but14=tk.Button(l,padx=5,pady=5,width=14,bg='green',fg='black',relief=tk.GROOVE,command=followMode,text="Follow mode ON",font=('helvetica 15 bold'))
        else : 
            but14=tk.Button(l,padx=5,pady=5,width=14,bg='red',fg='black',relief=tk.GROOVE,command=followMode,text="Follow mode Off",font=('helvetica 15 bold'))    
        but14.place(x = 1100, y = 0)
        time.sleep(0.5)

def recordVideo() :
    global videoRecording
    if videoRecording :
        videoRecording = False 
    else : 
        videoRecording = True

def updateRecordVideo() :
    while True :
        if videoRecording :
            but15 = tk.Button(l, padx = 5, pady=5, width=15,bg='green',fg='black',relief=tk.GROOVE,command= recordVideo,text='Video is recording...',font=('helvetica 15 bold'))
            but15.place(x = 900, y = 0)
        else : 
            but15 = tk.Button(l, padx = 5, pady=5, width=15,bg='green',fg='black',relief=tk.GROOVE,command= recordVideo,text='Record Video',font=('helvetica 15 bold'))
            but15.place(x = 900, y = 0)
        time.sleep(1)

def streamBegin() :  
    writer= cv2.VideoWriter('basicvideo.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (680,480))
 
    while True :
        frame_read = me.get_frame_read()
        myFrame = frame_read.frame
        gray = cv2.cvtColor(myFrame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        me.left_right_velocity = 0; me.for_back_velocity = 0; me.up_down_velocity = 0; me.yaw_velocity = 0
        if videoRecording :
            print("recording")
            writer.write(myFrame)
        if followmode :
            for (x,y,w,h) in faces :
                    if w > 100 :
                        # middle of person
                        middle_x = (x + (w/2))
                        middle_y = (y + (h/2))
                        
                        cv2.rectangle(myFrame, (x,y), (x+w, y+h), (255,0,0), 1, 1)
                            
                        if middle_x < 400:
                            #print("Go left")
                            dir = 1
                        elif middle_x > 500 :
                            #print("Go right")
                            dir = 2
                        elif middle_y < 320 :
                            #print("Go up")
                            dir = 3 
                        elif middle_y > 380:
                            #print("Go Down")
                            dir = 4
                        elif w > 350 :
                            dir = 5
                        elif w < 250 :
                            dir = 6
                        else :
                            dir = 0
                        
                        if dir == 1 : 
                            me.left_right_velocity = 0; me.for_back_velocity = 0; me.up_down_velocity = 0; me.yaw_velocity = -30
                        elif dir == 2 :
                            me.left_right_velocity = 0; me.for_back_velocity = 0; me.up_down_velocity = 0; me.yaw_velocity = 30
                        elif dir == 3 : 
                            me.left_right_velocity = 0; me.for_back_velocity = 0; me.up_down_velocity = 70; me.yaw_velocity = 0
                        elif dir == 4 :
                            me.left_right_velocity = 0; me.for_back_velocity = 0; me.up_down_velocity = -70; me.yaw_velocity = 0
                        elif dir == 0 :
                            me.left_right_velocity = 0; me.for_back_velocity = 0; me.up_down_velocity = 0; me.yaw_velocity = 0
                        elif dir == 5 :
                            me.left_right_velocity = 0; me.for_back_velocity = 60; me.up_down_velocity = 0; me.yaw_velocity = 0
                        elif dir == 6 :
                            me.left_right_velocity = 0; me.for_back_velocity = -60; me.up_down_velocity = 0; me.yaw_velocity = 0
                        
                        
                        
            reactThread = threading.Thread(target=react, args=(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity))
            
            if me.send_rc_control :
                reactThread.start()
            
        cv2.imshow("Result", myFrame)

        if cv2.waitKey(1) & 0xFF == ord('q') :
            me.land()
            break
    
    writer.release()
    cv2.destroyAllWindows()


l = tk.LabelFrame(root, text="Commands :", padx=20, pady=20)
l.pack(fill="both", expand="yes")

updateFollowModeThread = threading.Thread(target = updateFollowMode)
updateFollowModeThread.start()

recordVideoThread = threading.Thread(target = updateRecordVideo)
recordVideoThread.start()

leftWithArg = partial(left, 20)
but2=tk.Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=tk.GROOVE,command=leftWithArg,text='Left',font=('helvetica 15 bold'))
but2.place(x=300,y=100)

forwardWithArg = partial(forward, 20)
but3=tk.Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=tk.GROOVE,command=forwardWithArg,text='Forward',font=('helvetica 15 bold'))
but3.place(x=900,y=100)

backWithArg = partial(back, 20)
but4=tk.Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=tk.GROOVE,command=backWithArg,text='Back',font=('helvetica 15 bold'))
but4.place(x=900,y=200)

rightWithArg = partial(right, 20)
but5=tk.Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=tk.GROOVE,command=rightWithArg,text='Right',font=('helvetica 15 bold'))
but5.place(x=600,y=100)

but6=tk.Button(l,padx=5,pady=5,width=10,bg='red',fg='black',relief=tk.GROOVE,command=land,text='Land',font=('helvetica 15 bold'))
but6.place(x=20,y=75)

but7=tk.Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=tk.GROOVE,command=takeoff,text='Takeoff',font=('helvetica 15 bold'))
but7.place(x=20,y=10)


but8=tk.Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=tk.GROOVE,command=stream,text='Turn on Cam',font=('helvetica 15 bold'))
but8.place(x=20,y=150)

but9=tk.Button(l,padx=5,pady=5,width=10,bg='red',fg='black',relief=tk.GROOVE,command=exitt,text='Exit',font=('helvetica 15 bold'))
but9.place(x=20,y=225)

upwithArg = partial(up, 20)
but10=tk.Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=tk.GROOVE,command=upwithArg,text='Up',font=('helvetica 15 bold'))
but10.place(x=450,y=0)

downwithArg = partial(down, 20)
but11=tk.Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=tk.GROOVE,command=downwithArg,text='Down',font=('helvetica 15 bold'))
but11.place(x=450,y=200)

rotateWithArg = partial(rotate, 20)
but12=tk.Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=tk.GROOVE,command=rotateWithArg,text='Rotate to right',font=('helvetica 15 bold'))
but12.place(x = 1100, y = 100)

counterRotateWithArg = partial(counterRotate, 20)
but13=tk.Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=tk.GROOVE,command=counterRotateWithArg,text='Rotate to left',font=('helvetica 15 bold'))
but13.place(x = 1100,y = 200)

root.mainloop()
