from user_data import UserData
import pika


class SendData:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

    def send(self, user_data):
        self.channel.queue_declare(queue="check")
        self.channel.basic_publish(exchange='',
                                   routing_key='check',
                                   body=user_data)


class UserVerification:

    def __init__(self):
        self.__data = UserData()

    def registry(self) -> None:
        send = SendData()

        def callback(ch, method, properties, body):
            if body.decode() == "0":
                print("Неправильное имя пользователя")
            elif body.decode() == "1":
                print("Неправильный пароль")
            elif body.decode() == "2":
                print("Неправильный номер телефона")
            else:
                print(body.decode())
            send.channel.stop_consuming()

        self.__data.set_username()
        self.__data.set_password()
        self.__data.set_telephone_number()
        self.__data.set_is_registration(True)

        send.channel.queue_declare(queue="send")

        send.send(self.__data.serialization())

        send.channel.basic_consume(queue="send",
                                   on_message_callback=callback,
                                   auto_ack=True)
        send.channel.start_consuming()

    def login(self):
        self.__data.set_username()
        self.__data.set_password()
        self.__data.set_is_registration(False)

        send = SendData()
        send.send(self.__data.serialization())
