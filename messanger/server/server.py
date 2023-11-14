import pika, threading

connections = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connections.channel()


def send():
    while True:
        message = input("Сообщение: ")
        channel.basic_publish(exchange='',
                              routing_key='first',
                              body=message.encode('utf-8'))


def receive():
    def callback(ch, method, properties, body):
        print(f" [x] Получено {body.decode()}")

    channel.basic_consume(queue='second',
                          on_message_callback=callback,
                          auto_ack=True)
    channel.start_consuming()


def main():
    channel.queue_declare(queue="first")
    channel.queue_declare(queue="second")
    threads = []
    threads.append(threading.Thread(target=send))
    threads.append(threading.Thread(target=receive))

    for thread in threads:
        thread.start()


if __name__ == '__main__':
    main()
