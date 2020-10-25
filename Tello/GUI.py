import time
import cv2
from tkinter import *
import tkinter.messagebox
import threading 
import socket
import sys
import platform  
from functools import partial
from djitellopy import Tello
import time 

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')



startCounter = 1
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

root=Tk()
root.geometry('1366x768')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
root.title('Tello Drone')
frame.config(background='light blue')

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
        while True :
            if dir != 0 :
            time.sleep(1)
                me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)
            else : 
                pass


def streamBegin() : 
   
    while True :
        frame_read = me.get_frame_read()
        myFrame = frame_read.frame

        gray = cv2.cvtColor(myFrame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x,y,w,h) in faces :
                if w > 100 :
                    # middle of person
                    middle_x = (x + (w/2))
                    middle_y = (y + (h/2))
                    
                    cv2.rectangle(myFrame, (x,y), (x+w, y+h), (255,0,0), 1, 1)
                    '''              
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
                    '''
                    if w > 350 :
                        dir = 5
                    elif w < 250 :
                        dir = 6
                    else :
                        dir = 0
                    '''
                    if dir == 1 : 
                        me.left_right_velocity = -60; me.for_back_velocity = 0; me.up_down_velocity = 0; me.yaw_velocity = 0
                    elif dir == 2 :
                        me.left_right_velocity = 60; me.for_back_velocity = 0; me.up_down_velocity = 0; me.yaw_velocity = 0
                    elif dir == 3 : 
                        me.left_right_velocity = 0; me.for_back_velocity = 0; me.up_down_velocity = 60; me.yaw_velocity = 0
                    elif dir == 4 :
                        me.left_right_velocity = 0; me.for_back_velocity = 0; me.up_down_velocity = -60; me.yaw_velocity = 0
                    '''
                    if dir == 5 :
                        me.left_right_velocity = 0; me.for_back_velocity = 60; me.up_down_velocity = 0; me.yaw_velocity = 0
                    elif dir == 6 :
                        me.left_right_velocity = 0; me.for_back_velocity = 60; me.up_down_velocity = 0; me.yaw_velocity = 0
                    elif dir == 0 :
                        me.left_right_velocity = 0; me.for_back_velocity = 0; me.up_down_velocity = 0; me.yaw_velocity = 0

        reactThread = threading.Thread(target=react, args=(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity))
        
        if me.send_rc_control :
            reactThread.start()
        
        cv2.imshow("Result", myFrame)

        if cv2.waitKey(1) & 0xFF == ord('q') :
            me.land()
            break

l = LabelFrame(root, text="Commands :", padx=20, pady=20)
l.pack(fill="both", expand="yes")

leftWithArg = partial(left, 20)
but2=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=leftWithArg,text='Left',font=('helvetica 15 bold'))
but2.place(x=300,y=100)

forwardWithArg = partial(forward, 20)
but3=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=forwardWithArg,text='Forward',font=('helvetica 15 bold'))
but3.place(x=900,y=100)

backWithArg = partial(back, 20)
but4=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=backWithArg,text='Back',font=('helvetica 15 bold'))
but4.place(x=900,y=200)

rightWithArg = partial(right, 20)
but5=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=rightWithArg,text='Right',font=('helvetica 15 bold'))
but5.place(x=600,y=100)

but6=Button(l,padx=5,pady=5,width=10,bg='red',fg='black',relief=GROOVE,command=land,text='Land',font=('helvetica 15 bold'))
but6.place(x=20,y=75)

but7=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=takeoff,text='Takeoff',font=('helvetica 15 bold'))
but7.place(x=20,y=10)


but8=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=stream,text='Turn on Cam',font=('helvetica 15 bold'))
but8.place(x=20,y=150)

but9=Button(l,padx=5,pady=5,width=10,bg='red',fg='black',relief=GROOVE,command=exitt,text='Exit',font=('helvetica 15 bold'))
but9.place(x=20,y=225)

upwithArg = partial(up, 20)
but10=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=upwithArg,text='Up',font=('helvetica 15 bold'))
but10.place(x=450,y=0)

downwithArg = partial(down, 20)
but11=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=downwithArg,text='Down',font=('helvetica 15 bold'))
but11.place(x=450,y=200)

rotateWithArg = partial(rotate, 20)
but12=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=rotateWithArg,text='Rotate to right',font=('helvetica 15 bold'))
but12.place(x = 1100, y = 100)

counterRotateWithArg = partial(counterRotate, 20)
but13=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=counterRotateWithArg,text='Rotate to left',font=('helvetica 15 bold'))
but13.place(x = 1100,y = 200)
root.mainloop()
