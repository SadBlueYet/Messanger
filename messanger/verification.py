import socket

from user_data import UserData
import pika


class SendData:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_address = ('192.168.56.1', 12345)
        self.sock.connect(self.server_address)

    def send(self, user_data):
        self.sock.sendall(user_data.encode())

        data = self.sock.recv(1024)
        return data


class UserVerification:

    def __init__(self):
        self.__data = UserData()

    def registry(self) -> None:
        send = SendData()

        self.__data.set_username()
        self.__data.set_password()
        self.__data.set_telephone_number()
        self.__data.set_is_registration(True)
        body = send.send(self.__data.serialization())
        if body.decode() == "0":
            print("Неправильное имя пользователя")
        elif body.decode() == "1":
            print("Неправильный пароль")
        elif body.decode() == "2":
            print("Неправильный номер телефона")
        else:
            print(body.decode())

    def login(self):
        self.__data.set_username()
        self.__data.set_password()
        self.__data.set_is_registration(False)

        send = SendData()
        send.send(self.__data.serialization())
