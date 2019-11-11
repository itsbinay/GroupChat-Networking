# Multiuser Group Chatting Network
<hr>

A group chatting program that includes a server side and clients. This program is created based on running it on a MAC Terminal.

From a networking point-of-view, we perceive that everytime we connect to the internet and are sending message through an instant-messaging app, our messages are sent only once and it will definitely reach our target without any loss of message.

<img width="300" alt="Screenshot 2019-11-12 at 12 29 49 am" src="https://user-images.githubusercontent.com/44058187/68603747-e1c39500-04e3-11ea-8480-0883137f4a82.png">

However, that is not the case. In a computer network, this so called ***"reliable channel"*** doesn't really exist, only ***"unreliable channel"*** exist. In fact, whenever we send data, or in this case , "message", it is not guaranteed that our message will reach our target fully. The data may arrive corrupt to our target or our data may be lost on the way. In order to deal with an ***"unrealiable channel"*** , we design a data transfer protocol to deal with the problems we have faced earlier.

<img width="300" alt="Screenshot 2019-11-12 at 12 29 43 am" src="https://user-images.githubusercontent.com/44058187/68604100-af666780-04e4-11ea-9c5e-0932b9ffe740.png">

This Group Chatting project aims to create a multiuser group chatting network that will tackle the problem of unreliable data transfer while concurrently allowing multiple user to connect to a real-time group chatting platform.
