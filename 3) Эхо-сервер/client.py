import socket
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def add_new_user():
    global sock

    name = str(input("Введите свое имя: "))
    sock.send(name.encode())
    password = str(input("Введите свой пароль: "))
    sock.send(password.encode())


def addr_port():
    addr = str(input("Введите IP-адрес компьютера: "))
    port_name = str(input("Введите порт, по которому хотите подключиться: "))

    if addr == '':
        addr = "localhost"
    if port_name == '':
        port_name = 9090
    return addr, int(port_name)


def input_password():
    global sock
    data = 0
    while data != "4":
        password = str(input(f"Введите пароль: "))
        sock.send(password.encode())
        data = sock.recv(1024).decode("UTF-8")


def main():
    global sock, answer
    address, port = addr_port()
    sock.connect((address, port))

    while True:
        try:
            msg = input("Введите сообщение: ")
            sock.send(msg.encode())
            try:
                data = sock.recv(1024)
                msg = data.decode("UTF-8")
                if msg == "1":
                    add_new_user()
                elif msg == "2":
                    input_password()

                elif msg == "3":
                    data = sock.recv(1024)
                    print("Message from host: ", data.decode("UTF-8"))
            except:
                pass
            if msg == "exit":
                break
        except KeyboardInterrupt:
            print("Вы отсоедины от сервера!")
            msg = "exit"
            sock.send(msg.encode())
            break

    sock.close()


if __name__ == "__main__":
    main()
