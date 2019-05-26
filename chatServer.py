#!/usr/bin/python
from Crypto.Cipher import AES
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import base64

clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def encryption(message):
	BLOCK_SIZE = 16
	secret = '`?.F(fHbN6XK|j!t'
	PADDING = '{'

	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

	EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

	cipher = AES.new(secret)
	encoded = EncodeAES(cipher, message)
	return encoded

def decryption(encryptedMessage):

	PADDING = '{'
	secret = '`?.F(fHbN6XK|j!t'

	DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))
	cipher = AES.new(secret)
	decoded = DecodeAES(cipher, encryptedMessage).decode("utf-8").rstrip(PADDING)
	return decoded

def accept_incoming_connections():
	while True:
		client, client_address = SERVER.accept()
		print("%s:%s has connected." %client_address)
		encrypted = encryption("Welcome to the chat!" + " Now type your name and press enter!")
		client.send(encrypted)
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
	name = client.recv(BUFSIZ)
	welcome = "Welcome %s! To exit, type {quit}." %decryption(name)
	client.send(encryption(welcome))
	msg = "%s has joined the chat!" %decryption(name)
	broadcast(msg)
	clients[client] = decryption(name)
	while True:
		msg = client.recv(BUFSIZ)
		decryptedmsg = decryption(msg)
		decryptedname = decryption(name)
		if decryptedmsg != "{quit}":
			broadcast(decryptedmsg, decryptedname+": ")
		else:
			client.send(encryption("{quit}"))
			client.close()
			del clients[client]
			broadcast(encryption("%s has left the chat" %decryptedname))
			break

def broadcast(decryptedmsg, prefix=""):
	for sock in clients:
		msg = prefix+decryptedmsg
		msg = encryption(msg)
		sock.send(msg)


if __name__ == "__main__":
    SERVER.listen(5)  
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start() 
    ACCEPT_THREAD.join()
    SERVER.close()