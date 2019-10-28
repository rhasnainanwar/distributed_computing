import socket
import json

commands = ["query", "add", "del"]

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect(('0.0.0.0', 8888))
response = client.recv(4096)

print(response.decode())
print("Choose from the following commands:")
print("\t1. Query a word")
print("\t2. Add a new word")
print("\t3. Remove a word")

while True:
	print("\n>", end=" ")
	command = int(input())

	word = input("Enter the word: ")
	if command == 1:
		data = {"command": commands[command-1], "word": word.lower()}
	elif command == 2:
		meanings = input("Enter the comma separated meanings list: ")
		data = {"command": commands[command-1], "word": word.lower(), "meanings": meanings}
	elif command == 3:
		data = {"command": commands[command-1], "word": word.lower()}

	client.send(json.dumps(data).encode())
	response = client.recv(1024)
	print("Response:", response.decode())

	print("Again? (Y/[n]):", end=" ")
	choice = input()
	if choice == "n":
		break