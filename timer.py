#!/usr/bin/env python

# signal.py

import signal
import time
import RPi.GPIO as GPIO



def handler(signum, frame):
   global init
   global ledState
   print ("signal {} at {:.3f}".format(signum, time.time()-init))
   ledState = not ledState
   GPIO.output(LED, ledState)

GPIO.setmode(GPIO.BCM)
LED = 17
ledState = False
GPIO.setup(LED,GPIO.OUT)

signal.signal(signal.SIGALRM, handler)

init = time.time()

signal.setitimer(signal.ITIMER_REAL, 0.01, 1)

start = time.time()

while (time.time() - start) < 10:
   time.sleep(1)

signal.setitimer(signal.ITIMER_REAL, 0) # Disable the alarm
