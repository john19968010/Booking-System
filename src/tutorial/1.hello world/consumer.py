import pika, sys, os
from time import sleep

""" acknowledgement
Task will lost if consumer is terminated before task is completed.
Due to we set auto_ack=True, so RabbitMQ will delete the message from the queue as soon as it is delivered.
"""


def main():
    cred = pika.credentials.PlainCredentials(username="admin", password="admin")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=cred)
    )
    channel = connection.channel()

    channel.queue_declare(queue="hello")

    def callback(ch, method, properties, body):
        sleep(2)
        print(f" [x] Received {body}")

    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
