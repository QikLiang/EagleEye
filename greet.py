#!/usr/bin/env python3

from communicate import communicator
import pyttsx3
import time

def greet(message):
    name = str(message.payload, 'ascii')
    if name == "Qi":
        name = "Chee"

    engine = pyttsx3.init()
    engine.say('Hello ' + name)
    engine.runAndWait()

receiver = communicator(False, greet)

while True:
    time.sleep(1)
