BSP 03 of the student Paul Houssel 

**-------------------------------------**

This repository will explain the organisation of my technical 
delivrable.
In this repository you can find two folders :
    - AI :
        - edgeDetection.py :
            Python script I wrote in order to learn the opencv module on python.
            This script allows me to capture my webcan and recognise the edges present
            in the video 
        - faceDetection.py
            Creation of a tracking algorithm. Not optimised, it is really slow.
            Recognises face with a trained opencv model and then attempts to track them.
            The script can recognise multiple persons in one video. In function of the person face size it will determine which person to follow.
            This file was just an experimentation.
        - haarcascade_frontalface_default.xml :
             XML file storing data (a lot) about
            a trained AI model that is able to recognise faces.
            source : https://github.com/anaustinbeing/haar-cascade-files
        - peopleDetection.py :
            Same as 'faceDetection.py' with another trained opencv model
            that is able to recognize faces. This model is less efficient 
            then the other one.


    - Tello :
        This folder contains all the code related to the tello drone.
        - GUI.py : Python script that I build to experiment with the tkinter
        python module. This GUI was only experimental to familiarize myself 
        with the module.
        - GUI2.py : Python script running a Graphical User Interface in which 
        the user can control the drone with the commands. The user can also 
        see the live feed from the drone webcam.
        Furthermore, the drone is able to recognize the users face and (for the
        moment) go down or up in function of the users position in the frame
        - Tello.py : Python program in which the user can communicate with the 
        drone. Same principle as GUI.py, however the user has not access to a 
        GUI. This script is also not optimised, the difference between the two 
        script reaction is clearly visible
        - Tello SDK Documentation EN_1.3_1122.pdf : Official Documentation from
        DJI electronics. This tells us how to send and receive UDP packets 
        from and to the tello drone.
        - haarcascade_frontalface_default.xml : XML file storing data (a lot) about
        a trained AI model that is able to recognise faces.
        source : https://github.com/anaustinbeing/haar-cascade-files

Guide to use GUI2.py :

    With this python script you will be able to control the tello drone with the 
    help of a GUI :
        - Install the script 
        - Install all necessary python modules with the pip command on your terminal
        - Turn on your drone
        - Connect your PC's wifi antenna to the Tello network (name : TELLOXXXXX)
        - Run the python script on your pc
        - The GUI will open on your screen

**-------------------------------------**

Written by Paul Houssel