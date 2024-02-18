import pika
import pika.credentials
import sys


cred = pika.credentials.PlainCredentials(username="admin", password="admin")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=cred)
)
channel = connection.channel()
channel.exchange_declare(exchange="logs", exchange_type="fanout")

"""
# https://rabbitmq.com/queues.html
We don't need to declare a queue name in here, we use `fanout` to send all message.
so we let system to generate a random queue name for us. we get the queue name by `result.method.queue`
- exclusive: the queue will be deleted when the worker is disconnected (task will lost)
"""
result = channel.queue_declare(queue="", exclusive=True)

channel.queue_bind(exchange="logs", queue=result.method.queue)

message = " ".join(sys.argv[1:]) or "Send to all message."

# Not we set the exchange name to 'logs' just like what we declared in `channel.exchange_declare``
channel.basic_publish(exchange="logs", routing_key="", body=message)

print(f" [x] Sent {message}")

connection.close()
