import socket
import _thread as thread
import sys
import time

# Server Info
HOST = socket.gethostbyname('localhost')
PORT = 6789


'''Initialise the clientSocket and the address to connect to'''
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect((HOST,PORT))
clientSocket.settimeout(1.0)

print("Enter your name:")
username = input()

# Send the client's nickname
try:
    clientSocket.send(username.encode('utf-8'))
except:
    time.sleep(0)

print("Welcome to the chat group,",username)
print("===========================================")
Shut_down = False 

# Receive hanlder for the receive thread
def receive_handler(conn):
    global Shut_down
    '''Receiving message part'''
    while True:
        recv_message = ''   # Always init the iteration of while loop with an empty recv_message variable
        try:
            recv_message = clientSocket.recv(1024).decode('utf-8')  # receive the message
        except:
            if Shut_down is True:   # If this client wants to shutdown the thread , i.e. leave the group chat
                thread.exit()       # End this thread

        if recv_message:    # Only print if the message isn't empty
            print (recv_message)    # Print the received message
        time.sleep(0)


# Send Handler for the sending thread
def send_handler(conn):
    global Shut_down
    while True: 
        if Shut_down is True:   # If this client is ready to be shutdown
            thread.exit()       # End this thread
            break

        send_message = ''
        send_message = input()  # Read the terminal input and put it in the send_message variable

        if send_message:    # if the message isn't empty
            try:
                clientSocket.send(send_message.encode('utf-8')) # Send the message to the server
                if send_message == "exit":  # If the message is exit
                    Shut_down=True          # Get ready to shutdown all of this client's thread
            except:
                continue

        time.sleep(0)

# There are two separate threads to handle the receiving and sending on the client side because
# To avoid blocking by the "input()" function, such that the message that is received can be printed instantly,
# i.e. avoiding any message loss in the receiving side
thread.start_new_thread(receive_handler,(clientSocket,))    # Start the Receviing thread
thread.start_new_thread(send_handler,(clientSocket,))       # Start the Sending thread

while True: 
    if Shut_down is True:   # If the client is ready to shutdown, i.e. leave the chat
        time.sleep(1)       # Give it 1s delay before closing the socket to ensure everything regarding sending/receving message is properly ended
        break


clientSocket.close()        # Close this socket
print("You have logged off the chat!")
