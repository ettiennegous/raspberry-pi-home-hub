
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
while True:
    print("Led On")
    GPIO.output(12, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(18, GPIO.HIGH)
    time.sleep(3)
    print("LED OFF")
    GPIO.output(12, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    time.sleep(3)
