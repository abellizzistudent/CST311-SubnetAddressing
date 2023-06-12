# server.py
# CST 311: Introduction to Computer Networks
# May 31, 2022
# Programming Assignment #3EC
# Anna Bellizzi, David Debow, Justin Johnson, Ryan Parker
# Pacific Analytics

# Program description: connects to two clients and allows them to communicate, modelling a chat service

from socket import *
#for time.wait() in letterValueOfFirstClientResponse
import time

#allow threading
import threading

#global variables
# isFirstClient is bool to keep track if thread has the isFirstClient or client y
# true because isFirstClient is true at first
isFirstClient = True;

#semaphore lock
#nothing at 0, go at 1, loop until 2
continueLock = 0

# sockets (0 == X, 1 == Y)
connectionSockets = []
bothConnected = False

def join():
  #declare global variables so locals don't take precedent
  global isFirstClient
  global continueLock
  global bothConnected

  # placeOfConnection is holder where x is first or second, for Accepted placeOfConnection connection, 
  placeOfConnection = ""
  # initialLetter defines if it is X or Y client, initialize as A to know if it works
  initialLetter = "A"
  # isFirstClient is iniatially true global variable
  # flips to false, after first pass of if statement
  # First client will be set to X, and second client set to Y
  if (isFirstClient == True):
    initialLetter = "X"
    placeOfConnection = "first"
  else:
    initialLetter = "Y"
    placeOfConnection = "second"
  isFirstClient = False

  # Setup greeting by server with variables initialLetter and placeOfConnection
  # announced by both threads
  greetingOne = "Accepted "+placeOfConnection+" connection, calling it client "+initialLetter

  # wait message is sent back to client
  wait = "Client "+initialLetter+" connected"
   
  connectionSocket, addr = serverSocket.accept()

  connectionSockets.append(connectionSocket)
  
  # print Accepted first connection, calling client x or
  # print Accepted second connection, calling client y
  print(greetingOne)
  
  # semaphore type lock
  continueLock += 1
  # on first loop check first clients letter
  
  # first client to answer loops until second client answers
  while(continueLock<2):
    time.sleep(0.1)
  
  connectionSocket.send(wait.encode())
  
  # if this threrad is client Y 
  # then print out a waiting to receive message once by the Server
  # This is printed after both have connections have been accepted
  if(initialLetter == "Y"):
    print ("")
    print ("Waiting to receive message from client X and client Y....")
    print ("")
  
  bothConnected = True
  running = True
  
  while(running == True):
    # get response from client
    # print out client letter and message
    response = connectionSocket.recv(1024).decode()

    letteredResponse = "Client "+initialLetter+": "+response
    print(letteredResponse)
    
    if not bothConnected:
      running = False
      break
    
    if (initialLetter == "X"):
      connectionSockets[1].send(letteredResponse.encode())
    else:
      connectionSockets[0].send(letteredResponse.encode())

    if(response == "bye"):
      running = False
      time.sleep(0.1)
      connectionSockets[0].send("SHUTDOWN".encode())
      connectionSockets[1].send("SHUTDOWN".encode())
  
  # Only print on second thread
  if (initialLetter == "Y"):
    print(" ")
    print("Waiting a bit for clients to close their connections")
  # wait two seconds
  time.sleep(2)
  if (initialLetter == "Y"):
    print("Done.")
  
  # close connection to both
  connectionSocket.close()
  bothConnected = False
  

if __name__ == "__main__":
  serverPort = 12000
  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.bind(('', serverPort))
  serverSocket.listen(1)

  #greeting message
  print("The server is ready to receive 2 connections....")
  print("")

  #create threads
  one = threading.Thread(target=join)
  two = threading.Thread(target=join)

  #start threads
  one.start()
  two.start()

  #run until complete
  one.join()
  two.join()
  
  