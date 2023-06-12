# client.py
# CST 311: Introduction to Computer Networks
# May 31, 2022
# Programming Assignment #3EC
# Anna Bellizzi, David Debow, Justin Johnson, Ryan Parker
# Pacific Analytics
# Client that connects to a server
# Sends a message to the server
# receives messages from the server
# sends message from one client to another

from socket import *
import time
import threading

serverName = '10.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

modifiedSentence = clientSocket.recv(1024)
print("From Server: ", modifiedSentence.decode())

running = True

def sendMessage():
  global running
  while(running):
    sentence = input()
    clientSocket.sendto(sentence.encode(),(serverName, serverPort))

def receiveMessage():
  global running
  while(running):
    modifiedSentence = clientSocket.recv(1024)
    response = modifiedSentence.decode()
    if(response == "SHUTDOWN"):
      running = False
      print("Shutting Down")
    else:
      print(response)
    
sendThread = threading.Thread(target=sendMessage)
receiveThread = threading.Thread(target=receiveMessage)

#start threads
sendThread.start()
receiveThread.start()

#run until complete
sendThread.join()
receiveThread.join()

clientSocket.close()
