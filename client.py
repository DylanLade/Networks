import socket
import select
import errno
import sys

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 2577

my_username = input("Username: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
client.setblocking(False)

username = my_username.encode('utf-8')
username_header = F"{len(username) :< {HEADER_LENGTH}}".encode('utf-8')
client.send(username_header + username)

while True:
	message = input(F"{my_username} > ")

	if message:
		message = message.encode('utf-8')
		message_header = F"{len(message) :< {HEADER_LENGTH}}".encode('utf-8')
		client.send(message_header + message)

	try:
		while True:
			username_header = client.recv(HEADER_LENGTH)
			if not len(username_header):
				print("Connection closed by the server")
				sys.exit()

			username_length = int(username_length.decode('utf-8').strip())
			username = client.recv(username_length).decode('utf-8')

			message_header =  client.recv(HEADER_LENGTH)
			message_length = int(message_header.decode('utf-8').strip())
			message = client.recv(message_length).decode('utf-8')

			print(F"{username} > {message}")

	except IOError as e:
		if e.errno != errno.EAGAIN or e.errno != errno.EWOULDBLOCK:
			print('Reading error', str(e))
			sys.exit()
		continue

	except Exception as e:
		print('General error', str(e))
		sys.exit()
		


