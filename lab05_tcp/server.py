import socket
import sys
import threading
import json
from datetime import datetime

HOST = '' # all availabe interfaces
PORT = 8888 # arbitrary non privileged port 
lock = threading.RLock()

dictionary = {}

def handle_request(request):
	command = request["command"]

	if command == "query":
		if request["word"] in dictionary:
			return request["word"] + " => " + dictionary[request["word"]]
		else:
			return "ERROR: '" + request["word"] + "' not found!"

	elif command == "add":
		if request["word"] in dictionary:
			return "ERROR: '" + request["word"] + "' is already in dictionary!"
		else:
			lock.acquire()
			try:
				dictionary[request["word"]] = request["meanings"]
				print(request["word"], "added to dictionary!")
			except:
				return "ERROR: unable to add '" + request["word"] + "'"
			lock.release()
			return "INFO: '" + request["word"] + "' added successfully!"

	elif command == "del":
		if request["word"] not in dictionary:
			return "ERROR: '" + request["word"] + "' not found!"
		else:
			lock.acquire()
			try:
				del dictionary[request["word"]]
				print(request["word"], "added to dictionary!")
			except:
				return "ERROR: unable to delete '" + request["word"] + "'"
			lock.release()
			return "INFO: '" + request["word"] + "' removed successfully!"

def client_thread(conn, ip):
	conn.send("Welcome to the Dictionary Server!\n".encode())

	while True:
		try:
			data = conn.recv(4096)
			if not data:
				break
			request = json.loads(data)
			reply = handle_request(request)
			print(datetime.now(), "-", reply)
			conn.sendall(reply.encode())
		except ConnectionResetError as e:
			break
	print(ip,"left.")
	conn.close()


try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
	print("Could not create socket. Error Code: ", str(msg[0]), "Error: ", msg[1])
	sys.exit(0)

print("[-] Socket Created")

# bind socket
try:
	s.bind((HOST, PORT))
	print("[-] Socket Bound to port " + str(PORT))
except socket.error as msg:
	print("Bind Failed. Error Code: {} Error: {}".format(str(msg[0]), msg[1]))
	sys.exit()

s.listen(10)
print("Listening...")


while True:
	# blocking call, waits to accept a connection
	conn, addr = s.accept()
	print("[-] Connected to " + addr[0] + ":" + str(addr[1]))

	threading.Thread(target=client_thread, args=(conn,addr[0] + ":" + str(addr[1]))).start()

s.close()