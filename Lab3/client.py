import socket
import errno
import sys

host=socket.gethostname()
IP = socket.gethostbyname(host)
PORT = 14878

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	client.connect((IP, PORT))
except Exception as e:
	print("Connection to server failed : ", str(e))

while True:
	try:
		message = input()

		if not message:
			continue
		if message == "quit":
			sys.exit()
		if message == "logout":
			client.close()
			sys.exit()
		else:
			client.send(message.encode("utf-8"))

	except Exception as e:
		print('General error in message send : ', str(e))
		sys.exit()
	
	try:
		recieve = client.recv(1024)

		if not recieve:
			continue
		if recieve == "logout":
			sys.exit()
		else:
			print(recieve.decode("utf-8"))

	except Exception as e:
		print('General error in message recieve : ', str(e))
		sys.exit()


