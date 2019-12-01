from multiprocessing import Process, Pipe
from os import getpid
from random import randint


def send(pipe, pid, counter):
    pipe.send((counter))
    print('\nMessage sent from ' + str(pid) + ' at local time: ' + str(counter))
    return counter


def recv(pipe, pid, counter):
    timestamp = pipe.recv()
    print('\n'+str(pid) + ' local time: '+ str(counter))
    counter = max(timestamp, counter) + 1
    print('Message received at ' + str(pid) + ' at updated local time: ' + str(counter))
    return counter


# random increment before receive shows the delay in message passing
# +1 before send shows the processing time

def process_one(pipe):
    pid = getpid()
    counter = randint(1,10)
    counter = send(pipe, pid, counter)
    counter += randint(1,5)
    counter = recv(pipe, pid, counter)
    counter += 1
    counter = send(pipe, pid, counter)
    counter += randint(1,5)
    counter = recv(pipe, pid, counter)


def process_two(pipe):
    pid = getpid()
    counter = 0
    counter = recv(pipe, pid, counter)
    counter += 1
    counter = send(pipe, pid, counter)
    counter += randint(1,5)
    counter = recv(pipe, pid, counter)
    counter += 1
    counter = send(pipe, pid, counter)


if __name__ == '__main__':
	pipe12, pipe21 = Pipe()

	process1 = Process(target=process_one, 
					   args=(pipe12,))
	process2 = Process(target=process_two, 
					   args=(pipe21,))

	process1.start()
	process2.start()

	process1.join()
	process2.join()