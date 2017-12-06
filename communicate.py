from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import threading


# General message notification callback
def customOnMessage(message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# Suback callback
def customSubackCallback(mid, data):
    print("Received SUBACK packet id: " + str(mid))


# Puback callback
def customPubackCallback(mid):
    print("Received PUBACK packet id: ")
    print(mid)
    print("++++++++++++++\n\n")


host = "a1vgqh9vgvjzyh.iot.us-east-1.amazonaws.com"
rootCAPath = "root-CA.crt"
certificatePath = "EagleEyeSpeaker.cert.pem"
privateKeyPath = "EagleEyeSpeaker.private.key"
useWebsocket = False
topic = "eagleeye/frs"

class communicator:
    def __init__(self, sender, onMessageReceived):
        self.sender = sender
        if sender:
            self.clientId = "transmit"
        else:
            self.clientId = "receive"
        self.finished = False
        def callback(result):
            self.finished = onMessageReceived(result)
        self.onMessageReceived = callback
        self.setup()

    def sendMessage(self, message):
        self.myAWSIoTMQTTClient.publishAsync(topic, message, 1, ackCallback=customPubackCallback)

    def setup(self):
        # Init AWSIoTMQTTClient
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.clientId)

        self.myAWSIoTMQTTClient.configureEndpoint(host, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        self.myAWSIoTMQTTClient.onMessage = self.onMessageReceived

        # Connect and subscribe to AWS IoT
        self.myAWSIoTMQTTClient.connect()
        # Note that we are not putting a message callback here. We are using the general message notification callback.
        if not self.sender:
                self.myAWSIoTMQTTClient.subscribeAsync(topic, 1, ackCallback=customSubackCallback)
