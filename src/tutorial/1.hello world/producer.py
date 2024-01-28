import pika
import pika.credentials


cred = pika.credentials.PlainCredentials(username="admin", password="admin")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=cred)
)
channel = connection.channel()


channel.queue_declare(queue="hello")

for i in range(100):
    channel.basic_publish(exchange="", routing_key="hello", body=f"Hello World{i}!")
    print(f" [x] Sent 'Hello World{i}!'")
connection.close()
