from gpiozero import LED
from gpiozero import MotionSensor
from gpiozero import Button
from time import sleep
import subprocess
import threading
from threading import Thread

pir = MotionSensor(21)
turnOffDelay = 3
sampleRate = 3
screenOn = True
firstRun = True
debug = False

def PrintMessage(msg):
    if(debug):
        print(msg)           

while True:
    try:
        PrintMessage("Sample")
        if(pir.motion_detected):

            if not(screenOn):
                #subprocess.call(["/home/pi/rpi-toggle-screen.sh","on"])
                PrintMessage("Screen On")
                screenOn = True
            sleep(turnOffDelay)
        else:
            if(screenOn):
                #subprocess.call(["/home/pi/rpi-toggle-screen.sh","off"])
                PrintMessage("Screen Off")
                firstRun = False
                screenOn = False
        sleep(sampleRate)
    except KeyboardInterrupt:
        break
