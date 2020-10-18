# Communication script with tello drone, connected via TELLO wifi network



print ('\r\n\r\nTello drone communication tool\r\n')

print("...importing modules...")

import threading 
import socket
import sys
import time
import platform  
import cv2
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


print("Modules imported")

print("...Initialiasing UDP server to get video stream....")

drone_videostream = cv2.VideoCapture('udp://@0.0.0.0:11111')

print("Server initialised")

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


def receiveStream() :
    print("...receiving stream...")

    while True :        
        try :
            ret, frame = drone_videostream.read()
        except Exception :
            print(Exception)


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x,y,w,h) in faces :
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 3)

            # compute the middle of the frame
            height, width, channels = frame.shape
            middle_x_frame = height/2
            middle_y_frame = width/2
            # middle of person
            middle_x = (x + w)/2
            middle_y = (y + h)/2
            # offset between center and person
            offset_x = middle_x - middle_x_frame
            offset_y = middle_y - middle_y_frame         
          

        cv2.imshow("LiveStream", frame)
        
        if cv2.waitKey(25) & 0xFF == ord('q') :
            break
    cap.release()
    cv2.destroyAllWindows()
 

def detectPerson(x,y,w,h, frame):
    cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 3)

    # compute the middle of the frame
    height, width, channels = frame.shape
    middle_x_frame = height/2
    middle_y_frame = width/2
    # middle of person
    middle_x = (x + w)/2
    middle_y = (y + h)/2
    # offset between center and person
    offset_x = middle_x - middle_x_frame
    offset_y = middle_y - middle_y_frame


    scale = w-x
    cv2.putText(frame, "Followed Person", (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
    
def receiving():
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break

def battery_level() :
    # autoland if batterylevel is below 5 percent
    while True :
        msg = "battery?"
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
        data, server = sock.recvfrom(1518)
        batteryLevel = data.decode(encoding="utf-8")
        print("The battery level is sufficient, " + batteryLevel + " %")
       
        if int(batteryLevel) < 5 :
            msg = "land"
            msg = msg.encode(encoding="utf-8") 
            sent = sock.sendto(msg, tello_address)
       

receiveStreamThread = threading.Thread(target=receiveStream)
print ("...initialiazing connection with tello drone...")

message = "command"
message = message.encode(encoding="utf-8") 
sent = sock.sendto(message, tello_address)



print("Connection established")

#create a thread that will excute the receiving() function
receiveThread = threading.Thread(target=receiving)
receiveThread.start()

'''
# create a new thread to get async work done
batteryThread = threading.Thread(target=battery_level)
batteryThread.start()
'''

while True :
    message = input(str("Enter a command :\r\n"))
    if message == "streamon":
        message = message.encode(encoding="utf-8")         
        sent = sock.sendto(message, tello_address)
        time.sleep(3)
        receiveStreamThread.start()

    else :    
        message = message.encode(encoding="utf-8") 
        sent = sock.sendto(message, tello_address)


