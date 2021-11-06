import socket
import errno
import random
import logging

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w")
users = []
auth = {}

def add_new_user(conn):
	global sock, users
	sock.sendto(str.encode("1"), (conn))
	name = sock.recv(1024).decode("UTF-8")
	password = sock.recv(1024).decode("UTF-8")
	users.append([name, password, conn[0]])
	return (name)

def read_file():
	global users
	with open("users.txt", mode="r", encoding="UTF-8") as u:
		file = u.readlines()
		for i in range(len(file)):
			file[i] = file[i].strip("\n")
			file[i] = file[i].split(";")
	users = file

def write_in_file():
	global users
	with open("users.txt", mode="w", encoding="UTF-8") as u:
		for i in range(len(users)):
			data = users[i][0] + ";" + users[i][1] + ";" + users[i][2] + "\n"
			u.writelines(data)

def check_port():
	global sock
	try:
		port = int(input("Введите порт, который хотите открыть: "))
		logging.info(f"Введите порт, который хотите открыть: {port}")
		sock.bind(('', port))
	except socket.error as e:
		if(e.errno == errno.EADDRINUSE):
			logging.exception("Данный порт уже занят!")
			while True:
				try:
					port = random.randint(0, 65535)
					sock.bind(('', port))
					logging.info(f"Новый порт: {port}")
					print("Новый порт: ", port)
					break
				except:
					continue
	print(f"Слушаю порт: {port}")
	logging.info(f"Слушаю порт: {port}")

def func(conn):
	global users, auth
	for i in range(len(users)):
		if(conn[0] == users[i][2]):
			msg_name = users[i][0]
			if(msg_name not in auth.keys()):
				while (True):
					sock.sendto(str.encode("2"), (conn))
					password = sock.recv(1024).decode("UTF-8")
					if(password == users[i][1]):
						auth[msg_name] = 1
						sock.sendto(str.encode("4"), (conn))
						break
			break
	else:
		msg_name = add_new_user(conn)
		auth[msg_name] = 1
	return (msg_name)

def main():
	global sock, users
	read_file()
	check_port()
	while True:
		try:
			data, conn = sock.recvfrom(1024)
			logging.info(conn)
			msg = data.decode("UTF-8")
			msg_name = func(conn)
			if(data.decode("UTF-8") == "exit"):
				sock.close()
				break
			if(msg == ""):
				logging.info(f"Message: {msg}")
				continue
		except KeyboardInterrupt:
			sock.close()
			break
		else:
			logging.info(f"Message from {msg_name}: {msg}")
			print(f"Message from {msg_name}: {msg}")
			msg = input("Введите сообщение: ")
			sock.sendto(str.encode("3"), (conn))
			sock.sendto(msg.encode(), (conn))

	write_in_file()

if __name__ == "__main__":
	main()
