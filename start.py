from gpiozero import LED
from gpiozero import MotionSensor
from gpiozero import Button
from time import sleep
import subprocess
import threading
from threading import Thread

led1 = LED(18)
led2 = LED(23)
led3 = LED(24)
led4 = LED(25)
led5 = LED(12)

allLeds = [led1, led2, led3, led4, led5]
sequenceOff = [[2], [1,3], [0,4]]
sequenceOn = [[0], [1], [2], [3], [4], [3], [2], [1]]


pir = MotionSensor(16)

ledDelay1 = 0.05
ledDelay2 = 0.5
turnOffDelay = 5
screenOn = False
firstRun = True
debug = True
useLeds = True
sampleRateSec = 10

def PrintMessage(msg):
    if(debug):
        print(msg)

class MyButton:  
    def __init__(self, pin):
        self._running = True
        self._pin = pin
        self._button = Button(pin) 

    def terminate(self):  
        self._running = False  

    def run(self):
        while self._running:
            if(self._button.is_pressed):
                PrintMessage('Button ' + str(self._pin))
            

class MyLeds:
    def __init__(self, sequence, delay):
        self._running = True
        self._sequence = sequence
        self._delay = delay
        self._sequenceoff = [[2], [1,3], [0,4]]
        self._sequenceon = [[0], [1], [2], [3], [4], [3], [2], [1]]

    def terminate(self):  
        self._running = False  

    def run(self):
        while self._running:
            for myStep in self._sequence:
                for myLed in allLeds:
                    myLed.off()
                for myLed in myStep:
                    allLeds[myLed].on()
                    PrintMessage('Turn on ' + str(myLed))
                sleep(self._delay)

ScreenInstOn = MyLeds(sequenceOn, ledDelay1)
ScreenInstOff = MyLeds(sequenceOff, ledDelay2)
Button1Inst = MyButton(20)
Button2Inst = MyButton(5)

Button1Thread = Thread(target=Button1Inst.run)
Button1Thread.start()

Button2Thread = Thread(target=Button2Inst.run)
Button2Thread.start()

while True:
    try:
        if(pir.motion_detected):
            PrintMessage('Motion detected')
            if not(screenOn):
                subprocess.call(["/home/pi/rpi-toggle-screen.sh","on"])
                screenOn = True
                ScreenInstOff.terminate()
                ScreenInstOn.terminate()
                if(useLeds):
                    ScreenInstOn = MyLeds(sequenceOn, ledDelay1)
                    ScreenOnThread = Thread(target=ScreenInstOn.run)
                    ScreenOnThread.start()
            sleep(turnOffDelay)
        else:
            PrintMessage('No Motion')
            if(screenOn):
                ScreenInstOff.terminate()
                ScreenInstOn.terminate()
                if(useLeds):
                    ScreenInstOff = MyLeds(sequenceOff, ledDelay2)
                    ScreenOffThread = Thread(target=ScreenInstOff.run)
                    ScreenOffThread.start()
                subprocess.call(["/home/pi/rpi-toggle-screen.sh","off"])
                firstRun = False
                screenOn = False
        sleep(sampleRateSec)
    except KeyboardInterrupt:
        break
