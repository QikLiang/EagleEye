#!/usr/bin/env python3

from communicate import communicator
import pyttsx3
import time

def greet(message):
    name = str(message.payload, 'ascii')
    print("Received", name)
    if name == "Qi":
        name = "Chee"

    speech = 'Hello ' + name

    if name == "Unknown":
        speech = "Unknown entity found"


    engine = pyttsx3.init()
    engine.say(speech)
    engine.runAndWait()

receiver = communicator(False, greet)

while True:
    time.sleep(1)
