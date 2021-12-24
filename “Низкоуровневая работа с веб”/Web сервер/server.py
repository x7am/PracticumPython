from threading import Thread
import socket
import logging
import random
import errno
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w", encoding="UTF-8")

def read_settings_file(conf="config.txt"):
	settings = {}
	with open(conf, 'r') as file:
		for line in file:
			line = line.strip('\n')
			left, right = line.split('=')
			settings[left] = right
		file.close()
	return (settings)

def start_server(settings):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.bind(("", int(settings['port'])))
		print(f"Using socket: {settings['port']}")
	except socket.error as e:
		if(e.errno == errno.EADDRINUSE):
			print("This port is already in use!")
			while True:
				try:
					port = random.randint(0, 65535)
					sock.bind(('', port))
					print(f"New port: {port}")
					break
				except:
					continue
	sock.listen(1)
	return sock

class MyServer(Thread):
	"""
	Класс, реализующий простой веб-сервер.
	"""
	def __init__(self, conn, addr, settings):
		Thread.__init__(self)
		self.__conn = conn
		self.__addr = addr
		self.__settings = settings

	def run(self):
		data = self.__conn.recv(int(self.__settings['max_val']))
		msg = data.decode()

		# print(msg)

		domen = ''
		for i in msg:
			domen = domen + i
			if(i == '\n'):
				break
		if(domen != ""):
			domen = domen.split(" ")[1]
		if(len(domen) == 0):
			return

		date = datetime.now()
		ext = 'html'
		if(domen == '/'):
			domen = "index"
			ext = "html"
		else:
			if ("." in domen):
				domen, ext = domen.split(".")

		if(ext == "html" or ext == "css" or ext == "js"):
			try:
				file = open("./" + domen + "." + ext, 'r')
				logging.info(f"{date} --- {self.__addr} --- {domen} --- 200")
			except FileNotFoundError:
				file = open("./404.html")
				logging.info(f"{date} --- {self.__addr} --- {domen} --- 404")
		else:
			file = open("./403.html")
			logging.info(f"{date} --- {self.__addr} --- {domen}.{ext} --- 403")

		message = file.read()

		answer = f"""
		HTTP/1.1 200 OK
		Connection: Keep-Alive
		Date: {date}
		Content-Type: text/html; charset=utf-8
		Content-Type: text/css; charset=utf-8
		Content-Type: text/javascript; charset=utf-8
		Server: SelfMadeServer v0.0.1
		Content-Length: {int(self.__settings['max_val'])}

		{message}
		"""

		self.__conn.send(answer.encode())

def main():
	settings = read_settings_file("config.txt")
	sock = start_server(settings)
	while True:
		conn, addr = sock.accept()
		NewConnect = MyServer(conn, addr, settings).start()

if __name__ == "__main__":
	main()