# Communication script with tello drone, connected via TELLO wifi network

print ('\r\n\r\nTello drone communication tool\r\n')

print("...importing modules...")

import threading 
import socket
import sys
import time
import platform  
import cv2


print("Modules imported")

print("...Initialiasing UDP server to get video stream....")

drone_videostream = cv2.VideoCapture('udp://@0.0.0.0:11111')

print("Server initialised")

# my local adress to receive UDP packets from tello DRONE
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

width = 320
height = 240


def receiveStream() :
    print("...receiving stream...")

    while True :        
        try :
            ret, frame = drone_videostream.read()
        except Exception :
            print(Exception)

        '''

        height, width, channels = frame.shape
        # draw a line every 100 pixels
        for x in range(0, width -1, 160):
            cv2.line(frame, (x, 0), (x, height), (255, 0, 0), 1, 1)
        for y in range(0, height, 120):
            cv2.line(frame, (0,y), (width,y), (255,0,0), 1, 1)
'''
      
      

        cv2.imshow("LiveStream", frame)
        if cv2.waitKey(25) & 0xFF == ord('q') :
            break
 

    cap.release()
    cv2.destroyAllWindows()


   
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



