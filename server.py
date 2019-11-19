import socket
import _thread as thread
import time
import sys

PORT = 6789
HOST = socket.gethostbyname('localhost')

message_buffer = [] # Message Buffer
index_buffer = []   # Index Buffer which will identify which user sent the message

new_user_list = []  #New User List Buffer

connection_list=[]  #All of the connection established
connection_bool=[]  #status of the connection

left_index=[]   #All of the thread_index no that has left the chat
left_index_bool=[]  #Status of announcing left members
username_list=[]    #All of the username joined in the chat

def left_chat(this_index):  # Function to identify if "this_index" has left the chat
    global left_index
    for loc in left_index:
        if this_index==loc:
            return True
    return False

def broadcastAll(): # Function to broadcast all messages in the buffer to all users in the connection
    global message_buffer
    global index_buffer
    global connection_list
    
    iterator = 0    # Iterator to go through all of the index_buffer, one by one, correlated to the message buffer index
    for msg in message_buffer:  # For every message left in the message_buffer list
        conn_index=0    #Connection index
        if msg:
            msg = "<"+username_list[index_buffer[iterator]]+">: "+msg   # Append the nickname infront of the message
        for conn in connection_list:  # Iterate through all of the connection
            if not left_chat(conn_index):   # If this connection hasn't left the group chat
                if conn_index!=index_buffer[iterator]: 
                    # Check if we need to send to this connection, i.e. if its the user that sent the "msg, no need to send"
                    if msg:
                        conn.send(msg.encode('utf-8'))
            conn_index+=1
        iterator+=1

    # Empty out all of the buffer and index
    message_buffer.clear()
    index_buffer.clear()

def broadcastAllNew(name):  # Function to broadcast "welcome message" to about a new member to all members connected in the chat
    global connection_list

    if name:
        name +=  " has just joined the chat!"
    conn_index = 0
    for conn in connection_list:    # Iterate through all connections
        if not left_chat(conn_index):   # check if this connection hasn't left the group chat
            if name:
                conn.send(name.encode('utf-8')) 
        conn_index+=1

def left_broadcast_done():  # See if broadcasting of all of the members who have left is done
    global left_index
    global left_index_bool
  
    for i in range(len(left_index)):
        if not left_index_bool[i]:
            return False
    return True

def broadcastLeft(this_index):  # Broadcast that "this_index" user has left the chat to all of the members connected in the chat
    global username_list
    global connection_list

    left_username = username_list[this_index]
    message = left_username + " has left the chat!"
    conn_index = 0
    for conn in connection_list:
        if conn_index!= this_index and not left_chat(conn_index):
            conn.send(message.encode('utf-8'))
        conn_index+=1


def broadcast_handler():    # Broadcast_thread Function handler
    # this will be a function/thread that will be running all the time once this program starts
    global message_buffer
    global left_index_bool
    global left_index
    global new_user_list

    while True:
        while len(new_user_list)!=0:    # Check if any new members joined the chat, in the new_members buffer
            broadcastAllNew(new_user_list.pop(0))
            
        if len(message_buffer)>0:   # Check if there is any message left in the message buffer
            broadcastAll()
        
        if not left_broadcast_done():   # If not all of the members that have left's notice hasn't been broadcasted
            for i in range(len(left_index)):
                if left_index_bool[i] is False:  #If haven't broadcasted, then broadcast
                    broadcastLeft(left_index[i])
                    left_index_bool[i]=True
                
def handle_client(conn,loc_index):  # Client_threads function handler
    global message_buffer
    global index_buffer
    global left_index
    global left_index_bool
    global connection_bool
    global username_list
    global new_user_list

    loc_message = ''

    #Local Variables
    joined = False  # identify for new clients
    end_handler = False # boolean variable to end the thread

    while True:
        if end_handler or not connection_bool[loc_index]:   # End the infinite loop in this thread
            print(username_list[loc_index],'is exiting the group chat!')
            break

        try:
            loc_message = conn.recv(1024).decode('utf-8')   #Get the new message
            if joined:
                print ("Recevied message from ",username_list[loc_index], " saying ", loc_message)

            if loc_message == "exit":   # If client wants to exit the chat
                print(username_list[loc_index],'is exiting the group chat!')
                end_handler = True  # Make this infinite loop in this client to quit
                connection_bool[loc_index]=False    # Clarify that this connection has been closed
                left_index.append(loc_index)    # Append this client's index into the left_index list
                left_index_bool.append(False)   # Append that this client's left group chat message HAS NOT been broadcasted
                print('loc message:',loc_message,' index:',loc_index, ' end_handler:',end_handler)
                continue
                

            if not joined: # New member joined, append his name to the new member list buffer and continue
                username_list.append(loc_message)
                new_user_list.append(loc_message)
                joined=True
                continue

            if not end_handler: # As long as this infinite loop isn't ready to be closed yet
                message_buffer.append(loc_message)  # Append the message to the message buffer
                index_buffer.append(loc_index)      # Append the client_index to the index buffer
                time.sleep(0)
        except:
            continue

    # Close the connection in this thread and end the thread  
    print('connection closed with ', username_list[loc_index])
    conn.shutdown(1)
    conn.close()
    sys.exit()

# Initialise the serverSocket          
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind((HOST,PORT))
serverSocket.listen()
print("Server has started listening...")

#Start a broadcasting_thread 
thread.start_new_thread(broadcast_handler,())

thread_index = 0 

while True:
    #Accepts the new connection and get its info
    connectionSocket, addr = serverSocket.accept()
    print('Connected by', addr[0],':',addr[1], " thread index: ",thread_index)

    #Some Connection info
    connection_list.append(connectionSocket)    
    connection_bool.append(True)

    #Start the client thread
    thread.start_new_thread(handle_client,(connectionSocket,thread_index))

    #Increment the thread index
    thread_index+=1

serverSocket.close()



