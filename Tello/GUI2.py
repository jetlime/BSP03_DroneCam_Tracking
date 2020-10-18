import time
import cv2
from tkinter import *
import tkinter.messagebox
import threading 
import socket
import sys
import platform  
from functools import partial


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

droneTookOf = False

height = 720
width = 960
middle_x_frame = height/2
middle_y_frame = width/2

root=Tk()
root.geometry('1366x768')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
root.title('Tello Drone')
frame.config(background='light blue')

print("...Initialiasing UDP server to get video stream....")
drone_videostream = cv2.VideoCapture('udp://@0.0.0.0:11111')
print("server Initialised")

# my local adress to send UDP packets from tello DRONE
host = ''
port = 9000
locaddr = (host,port) 
print("...creation of UDP socket...")
# Create a UDP socket (UDP Portocol to receive and send UDP packets from/to drone)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Got drone port and ip adress from network (explained in official SDK documentation)
tello_address = ('192.168.10.1', 8889)
print("UDP socket created")
sock.bind(locaddr)

def sending() :   
    message = "command"
    message = message.encode(encoding="utf-8") 
    sent = sock.sendto(message, tello_address)
    while True :
        message = input(str("Enter a command :\r\n"))
        send(message)

def send(message) :
    print('sending ' + message)
    message = message.encode(encoding="utf-8") 
    sent = sock.sendto(message, tello_address)

def receiving():
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break


def takeoff() :
    droneTookOf = True
    send("takeoff")

def up(y) : 
    send("up " + str(y))

def land() : 
    send("land")

def right() : 
    send("right 20")

def down(y) :
    send("down " + str(y))

def left() : 
    send("left 20")

def forward() :
    send("forward 20")

def back() :
    send("back 20")

def stream() :
    send("streamon")
    streambeginThread = threading.Thread(target=streamBegin)
    streambeginThread.start()
    
def exitt() :
    exit()
    send("streamoff")

def streamBegin() : 
    while True :        
        try :
            ret, frame = drone_videostream.read()
        except Exception :
            print(Exception)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if droneTookOf :
            for (x,y,w,h) in faces :

                # middle of person
                middle_x = (x + w)/2
                middle_y = (y + h)/2
                # offset between center and person
                offset_x = middle_x - middle_x_frame
                offset_y = middle_y - middle_y_frame        
                if offset_y > -180 :
                    down(20)
                elif offset_y < -200 :
                    up(20)    
                time.sleep(2)

        cv2.imshow("LiveStream", frame)
        
        if cv2.waitKey(25) & 0xFF == ord('q') :
            break
    cap.release()
    cv2.destroyAllWindows()

receiveThread = threading.Thread(target=receiving)
receiveThread.start()

sendThread = threading.Thread(target=sending)
sendThread.start()

l = LabelFrame(root, text="Commands :", padx=20, pady=20)
l.pack(fill="both", expand="yes")

but2=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=left,text='Left',font=('helvetica 15 bold'))
but2.place(x=300,y=100)

but3=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=forward,text='Forward',font=('helvetica 15 bold'))
but3.place(x=900,y=100)

but4=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=back,text='Back',font=('helvetica 15 bold'))
but4.place(x=900,y=200)

but5=Button(l,padx=5,pady=5,width=10,bg='green',fg='black',relief=GROOVE,command=right,text='Right',font=('helvetica 15 bold'))
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

root.mainloop()
