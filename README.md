# Chatroom

Simple chatroom program built in Python 3.7.3 that allows up to 5 users to connect to a chatroom where messages are broadcasted to every user currently in the room. The messages sent to the group chat are encrypted using AES to prevent someone from listening in on messages being sent because without AES messages would be in plain text.

# Important
- By default will automatically try to connect 127.0.0.1 on PORT 33000 if you click submit without setting the HOST and PORT fields
- You will need PyCrypto and Tkinter for this to run

# Usage
**Server Side** Python3 chatServer.py  
- This starts up the server and listens for connections  

**Client Side** Python3 chatClient.py  
- This starts up the client and asks you to enter the HOST IP and PORT to connect to  

