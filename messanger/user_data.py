from user_input import input_integer, input_password, input_username, input_telephone_number
import json, socket

"""
    Этот класс отвечает за получение и выдачу данных пользователя
"""


class UserData:

    def __init__(self):
        self.__username = None
        self.__password = None
        self.__telephone_number = None
        self.__is_registration = None
        self.__ip_address = socket.gethostbyname(socket.gethostname())

    def serialization(self):
        return json.dumps(self.__dict__)

    def set_is_registration(self, is_registration: bool):
        self.__is_registration = is_registration
    def set_username(self):
        self.__username = input_username()

    def set_password(self):
        self.__password = input_password()

    def set_telephone_number(self):
        self.__telephone_number = input_telephone_number()

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_telephone_number(self):
        return self.__telephone_number





