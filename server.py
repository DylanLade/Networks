import socket
import select

host=socket.gethostname()
IP = socket.gethostbyname(host)
PORT = 14878

#Set up the server and git it ready to connect hosts
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP, PORT))
server.listen(1)

#Accepts the client connection
client_socket, client_address = server.accept()
print(F"Accepted connection from {client_address[0]}:{client_address[1]}")

#Create the users struct for cheking login info
current_user = ""
users = []
file = open("users.txt","r+")
for line in file:
	temp = line
	tempparse = temp.split(',')
	users.append({"username": tempparse[0].rstrip(),
				  "password": tempparse[1].rstrip()})

# User check for use with login
def check_user(userID, password):
	for user in users:
		if userID == user['username'] and password == user['password']:
			print(F"{userID}'s login information has been verified")
			return userID
		else:
			client_socket.send(bytes("The user entered does not exist! Please check the login info or use the command newuser to create", "utf-8"))
		
# Creates a new user
def create_user(userID, password):
	try:
		if len(userID) > 32 and len(userID) < 1:
			client_socket.send(bytes("Username must be less than 32 characters", "utf-8"))
			return False

		if len(password) < 4 and len(password) > 8:
			client_socet.send(bytes("Password must be between 4 and 8 characters", "utf-8"))
			return False	

		users.append({"username": userID, "password": password})
		print(F"New user {userID} has been created")
		return userID	

	except:
		print("Create user has failed!")
		client_socket.send(bytes("Server Create user has failed", "utf-8"))

# Main chat loop
while True:
	if not client_socket:
		server.listen(1)
		client_socket, client_address = server.accept()
		print(F"Accepted connection from {client_address[0]}:{client_address[1]}")

	else:
		message = client_socket.recv(1024).decode("utf-8")
		parse = message.split()
		print(F"{parse[0]} command requested")
		print("...processing...")
		if parse[0] != "login" || "send" || "logout" || "newuser":
			client_socket.send(bytes("Previous command is not valid", "utf-8"))

	# Check sent message for login command
		if parse[0] == "login":
			try:
				current_user = check_user(parse[1], parse[2])
				client_socket.send(bytes(F"{current_user} has been signed in", "utf-8"))

			except IndexError:
				client_socket.send(bytes("Please provide a username and passsword to login", "utf-8"))
				continue

	# Check sent message for newuser command
		if parse[0] == "newuser":
			current_user = create_user(parse[1], parse[2])
			print(current_user + " has been created and signed in")
			client_socket.send(bytes(F"{current_user} has been created and signed in", "utf-8"))


	# Check sent messade got logout
		if parse[0] == "logout":
			print(current_user + " has been signed out")
			client_socket.send(bytes(F"{current_user} has been signed out", "utf-8"))
			client_socket.close()
			current_user = ""
			

	# Check sent message for send command
		if parse[0] == "send":
			if current_user == "":
				client_socket.send(bytes("A user must be signed in to send a message","utf-8"))
				continue
			else:
				del parse[0]
				sent = ' '.join(parse)
				print(F"Recieved message from {current_user} : {sent}")
				client_socket.send(bytes(F"{current_user} : {sent}", "utf-8"))

	# If the user quits, notifies server
		if parse[0] == "quit":
			print("Client has disconnected")