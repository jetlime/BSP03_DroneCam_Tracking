import numpy as np
import queue
from multiprocessing import Process, Queue
from queue import Empty
import cv2
from PIL import Image, ImageTk
import time
import tkinter as tk
import threading 
import socket
import sys
import platform

def quit_(root, process):
    process.terminate()
    root.destroy()


def update_image(image_label, queue):
   frame = queue.get()
   im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   a = Image.fromarray(im)
   b = ImageTk.PhotoImage(image=a)
   image_label.configure(image=b)
   image_label._image_cache = b  # avoid garbage collection
   root.update()

def update_all(root, image_label, queue):
   update_image(image_label, queue)
   root.after(0, func=lambda: update_all(root, image_label, queue))

#multiprocessing image processing functions-------------------------------------
def image_capture(queue):
   vidFile = cv2.VideoCapture(0)
   while True:
      try:
         flag, frame = drone_videostream.read()
         if flag==0:
            break
         queue.put(frame)
         cv2.waitKey(20)
      except:
         continue


def receiving():
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break

def send(message) :
    print('sending ' + message)
    message = message.encode(encoding="utf-8") 
    sent = sock.sendto(message, tello_address)

def sending() :
    while True :
        message = input(str("Enter a command :\r\n"))
        if message == "streamon":
            send(message)
            time.sleep(3)
        elif message == "q" :
            send("land")
        else :    
            send(message)


if __name__ == '__main__':
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

    message = "command"
    message = message.encode(encoding="utf-8") 
    sent = sock.sendto(message, tello_address)
    receiveThread = threading.Thread(target=receiving)
    receiveThread.start()

    sendingThread = threading.Thread(target=sending)
    sendingThread.start()
    queue = Queue()
    print('queue initialized...')
    root = tk.Tk()
    print('GUI initialized...')
    image_label = tk.Label(master=root)# label for the video frame
    image_label.pack()
    print('GUI image label initialized...')
    p = Process(target=image_capture, args=(queue,))
    p.start()
    print('image capture process has started...')
    # quit button
    quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root,p))
    quit_button.pack()
    print('quit button initialized...')
    # setup the update callback
    root.after(0, func=lambda: update_all(root, image_label, queue))
    print('root.after was called...')
    root.mainloop()
    print('mainloop exit')
    p.join()
    print('image capture process exit')