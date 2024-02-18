import pika
import pika.credentials
import sys


cred = pika.credentials.PlainCredentials(username="admin", password="admin")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=cred)
)
channel = connection.channel()


channel.queue_declare(queue="task_queue", durable=True)
message = " ".join(sys.argv[1:]) or "Hello World!"
# if exchange is not set(or set to an empty string ""), the message will be sent to default or nameless exchange,
# task will send to the queue with the same name as routing_key(if exists).
channel.basic_publish(
    exchange="",
    routing_key="task_queue",
    body=message,
    properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
)

print(f" [x] Sent {message}")

connection.close()
