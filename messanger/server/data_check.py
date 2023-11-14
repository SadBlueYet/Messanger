import pika
import threading
import hashlib
import phonenumbers
import json
import re
from database import UsersDB

connections = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connections.channel()


def send(status_code: str):
    channel.queue_declare(queue="send")
    channel.basic_publish(exchange='',
                          routing_key='send',
                          body=status_code.encode("utf-8"))


def receive():
    def callback( ch, method, properties, body):
        check(body.decode())

    channel.basic_consume(queue='check',
                          on_message_callback=callback,
                          auto_ack=True)
    channel.start_consuming()


def check(data):
    user = UserCheck(data)

    if not user.set_username():
        send("0")
        return
    if user.is_registration:
        if not user.check_password():
            send("1")
            return
        if not user.set_telephone_number():
            send("2")
            return
        user.add_user()
    else:
        if not user.checking_password_for_existence():
            send("1")
            return
    send("Верификация прошла успешно")
    print("Пользователь успешно зарегистрирован")


class UserCheck:
    def __init__(self, data):
        deserialization_data = json.loads(data)
        self.__username = deserialization_data['_UserData__username']
        self.__password = deserialization_data['_UserData__password']
        self.__telephone_number = deserialization_data['_UserData__telephone_number']
        self.is_registration = deserialization_data['_UserData__is_registration']
        self.__ip_address = deserialization_data['_UserData__ip_address']
        self.__db = UsersDB()

    def add_user(self):
        self.__db.set_user(self.__username,
                           self.__password,
                           self.__telephone_number,
                           self.__ip_address)

    def check_username(self):
        db_username = self.__db.find_username(self.__username)
        a = db_username.fetchone()
        if a is None:
            return True
        else:
            return False

    def set_username(self) -> bool:
        if self.is_registration and not self.check_username():
            print("Такое имя пользователя уже существует")
            return False
        if not self.is_registration and self.check_username():
            print("Не найдено такого пользователя")
            return False
        return True

    def check_password(self) -> bool:
        if not re.match("^[A-Za-z0-9]{8,}$", self.__password):
            print("Пароль должен состоять из латинских букв и цифр и быть не менее 8 символов")
            return False
        self.__password = hash_password(self.__password)
        return True

    def checking_password_for_existence(self) -> bool:

        db_password = self.__db.find_password(self.__username)
        if db_password is None or db_password[0] != hash_password(self.__password):
            print("Неправильный пароль.\nПопробуйте еще раз")
            return False
        else:
            return True

    def check_repetition_telephone_number(self) -> bool:

        db_telephone_number = self.__db.find_telephone_number(self.__telephone_number)
        a = db_telephone_number.fetchone()
        if a is None:
            return True
        else:
            return False

    def set_telephone_number(self) -> bool:
        while True:
            if not check_valid_telephone_number(self.__telephone_number):
                print("Неверный номер телефона")
                return False
            if not self.check_repetition_telephone_number():
                print("Такой телефон уже существует")
                return False
            return True


def hash_password(password: str) -> str:
    hash_object = hashlib.sha256()
    hash_object.update(password.encode('utf-8'))
    hashed_password = hash_object.hexdigest()
    return hashed_password


def check_valid_telephone_number(telephone_number: str) -> bool:
    try:
        phone = phonenumbers.parse(telephone_number, None)
        if phonenumbers.is_valid_number(phone):
            return True
        else:
            return False
    except phonenumbers.phonenumberutil.NumberParseException as e:
        print("Error:", str(e))
        return False


def main():
    channel.queue_declare(queue="check")

    receive()
    """channel.queue_declare(queue="second")
    threads = []
    threads.append(threading.Thread(target=send))
    threads.append(threading.Thread(target=receive)

    for thread in threads:
        thread.start()"""


if __name__ == '__main__':
    main()
