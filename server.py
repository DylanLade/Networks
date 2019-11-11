import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 2577

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((IP, PORT))

server.listen()

sockets_list = [server]

clients = {}


def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {"header": message_header,
                "data": client_socket.recv(message_length)}


    except:
    	return False


while True:
	read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

	for notified_socket in read_sockets:
		if notified_socket == server:
			client_socket, client_address = server.accept()

			user = recieve_message(client_socket)
			if user is False:
				continue

			sockets_list.append(client_socket)

			clients[client_socket] = user

			print(F"Accepted connection from {client_address[0]}:{client_address[1]} Username: {user['data'].decode('utf-8')}")

		else:
			message = recieve_message(notified_socket)

			if message is False:
				print(F"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
				sockets_list.remove(notified_socket)
				del clients[notified_socket]
				continue

			user = clients[notified_socket]
			print(F"Recieved message from {user['data'].decode('utf-8')} : {message['data'].decode(utf-8)}")
			for client in clients:
				if client_socket != notified_socket:
					client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

	for notified_socket in exception_sockets:
		sockets_list.remove(notified_socket)
		del clients[notified_socket]