import pyttsx3
from communicate import communicator
import time

def onMessageReceived(message):
    payload = str(message.payload, 'ascii')
    print(payload)
    if payload == "Qi":
        engine = pyttsx3.init()
        engine.say("It works!")
        engine.runAndWait()
        return True
    return False

receiver = communicator(False, onMessageReceived)

while not receiver.finished:
    time.sleep(1)
