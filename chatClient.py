#!/usr/bin/python
from Crypto.Cipher import AES
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
import tkinter
import base64

HOST = ''
PORT = ''

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

def receive():
	while True:	
		try:
			msg = client_socket.recv(BUFSIZ)
			msg = decryption(msg)
			msg_list.insert(tkinter.END, msg)

		except OSError:
			break

def send(event=None):
	msg = encryption(my_msg.get())
	my_msg.set("")
	client_socket.send(msg)
	if decryption(msg) == "{quit}":
		client_socket.close()
		top.quit()

def on_closing(event=None):
	my_msg.set("{quit}")
	send()

def on_click_HOST(event=None):
	entHost.delete(0, tkinter.END)
	entHost.config(fg='black')

def on_click_PORT(event=None):
	entPort.delete(0, tkinter.END)
	entPort.config(fg='black')

def on_click_entry(event=None):
	my_msg.set("")
	entry_field.config(fg='black')


def setValues():
	global HOST
	global PORT
	if HOST == '' and PORT == '':
		HOST = "127.0.0.1"
		PORT = 33000
	else:
		HOST = entHost.get()
		PORT = int(entPort.get())
	root.destroy()

root = tkinter.Tk()
root.title("Connection")
hostLabel = tkinter.Label(root, text="Enter HOST")
entHost = tkinter.Entry(root)
entPort = tkinter.Entry(root)
entHost.insert(0,"Enter HOST")
entPort.insert(0,"Enter PORT")
entHost.bind('<FocusIn>', on_click_HOST)
entPort.bind('<FocusIn>', on_click_PORT)
entHost.config(fg='grey')
entPort.config(fg='grey')
submit = tkinter.Button(root, text="Submit", command = setValues)
hostLabel.pack()
entHost.pack(side="left")
entPort.pack(side="left")
submit.pack()

x = (root.winfo_screenwidth() - root.winfo_reqwidth()-180) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()-150) / 2
root.geometry("+%d+%d" % (x, y))
root.mainloop()

top = tkinter.Tk()
top.title("Messenger")


BUFSIZ = 1024
ADDR = (HOST, PORT)

messages_frame = tkinter.Frame()
my_msg = tkinter.StringVar()
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand = scrollbar.set)

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.config(fg='grey')
entry_field.bind('<FocusIn>', on_click_entry)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
top.geometry('+%d+%d' % (x, y))

top.protocol("WM_DELETE_WINDOW", on_closing)

try:
	client_socket = socket(AF_INET, SOCK_STREAM)
	client_socket.connect(ADDR)
	receive_thread = Thread(target=receive)
	receive_thread.start()
	tkinter.mainloop()
except Exception as err:
	print("Failed to connect to server.")

