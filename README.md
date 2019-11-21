# Multiuser Group Chatting Network

> By Binay gurung

A group chatting program that includes a server side and clients. This program is created based on running it on a MAC Terminal.

From a networking point-of-view, we perceive that everytime we connect to the internet and are sending message through an instant-messaging app, our messages are sent only once and it will definitely reach our target without any loss of message.

<img width="300" alt="Screenshot 2019-11-12 at 12 29 49 am" src="https://user-images.githubusercontent.com/44058187/68603747-e1c39500-04e3-11ea-8480-0883137f4a82.png">

However, that is not the case. In a computer network, this so called ***"reliable channel"*** doesn't really exist, only ***"unreliable channel"*** exist. In fact, whenever we send data, or in this case , "message", it is not guaranteed that our message will reach our target fully. The data may arrive corrupt to our target or our data may be lost on the way. In order to deal with an ***"unrealiable channel"*** , we design a data transfer protocol to deal with the problems we have faced earlier.

<img width="300" alt="Screenshot 2019-11-12 at 12 29 43 am" src="https://user-images.githubusercontent.com/44058187/68604100-af666780-04e4-11ea-9c5e-0932b9ffe740.png">

This Group Chatting project aims to create a multiuser group chatting network that will tackle the problem of unreliable data transfer while concurrently allowing multiple user to connect to a real-time group chatting platform.

The current implementation of the project is done using the Transmission Control Protocol which has already implemented the 
**reliable data transfer** that will need to be implemented over a unreliable channel. 

#### Server Side
On the server-side, in order to deal with concurrent handling of clients of receiving and sending message, the current implementation of the server-side is as follows:
- 1 thread per client module (data received will be pushed into the **global** buffer)
- 1 thread to handle broadcasting to all of the connected clients in the group chat

#### Client Side
On the client-side, in order to avoid `input()` , an input blocking operations, from affecting the receivier-side of the client, the client-side is implemented as follows:
- 1 thread for receiving
- 1 thread for sending (i.e. sending the data inputted by the user)

#### How to run the program?
To run this groupChat platform, you must first start up the server-side of the network. To do so, go to the directory of the `server.py` file in terminal, and run the python script
i.e. `python server.py`

<img width="482" alt="Screenshot 2019-11-21 at 2 18 27 pm" src="https://user-images.githubusercontent.com/44058187/69312454-f6352980-0c69-11ea-83e6-54ca7d49a47a.png">

`Server has started listening...` indicates that the server is ready to accept connections from its clients.

To join the groupchat server, run the `client.py` python script on another terminal.

###### Client Side
<img width="479" alt="Screenshot 2019-11-21 at 2 23 17 pm" src="https://user-images.githubusercontent.com/44058187/69312654-87a49b80-0c6a-11ea-8149-768f9a57c65e.png">

After starting up the script, you can input your nickname for the groupchat to successfully join the chat.

###### Server Side
<img width="492" alt="Screenshot 2019-11-21 at 2 23 28 pm" src="https://user-images.githubusercontent.com/44058187/69312727-c20e3880-0c6a-11ea-9881-109065c4876b.png">

The server side will indicate that the user has connected the server and new thread has started is indicated.

If you would like to join more clients, feel free to open up more clients to join the chat.

###### Leaving the Group Chat
Once you are done using the chat, on the client side, type `exit` to exit the group chat. The connection handling is done by the server and the program is ended on the client side.

<img width="464" alt="Screenshot 2019-11-21 at 2 28 15 pm" src="https://user-images.githubusercontent.com/44058187/69312924-2f21ce00-0c6b-11ea-8519-2d70ca0259fe.png">
