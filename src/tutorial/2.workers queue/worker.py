import pika
from time import sleep

# Recover worker from consumer or RabbitMQ server is terminated.

"""acknowledgement
In the previous tutorial, we wrote a program that sends a single message. and set auto_ack=True, 
but this one, we set a proper acknowledgment from the worker by adding `ch.basic_ack(delivery_tag=method.delivery_tag)`, 
in the callback function. to ensure that the task will not lost. However, it only available in the same channel. 
"""

"""Message durability
So the `ch.basic_ack(delivery_tag=method.delivery_tag)` can prevent the message lost, but what if the RabbitMQ server is terminated?
We needs two do two things, firstly setting durable on the queue. `channel.queue_declare(queue='hello', durable=True)` , and then 
setting persistent on the message. `channel.basic_publish(exchange='', routing_key='hello', body=message, properties=pika.BasicProperties(
    delivery_mode = pika.DeliveryMode.Persistent))`
NOTE: RabbitMQ doesn't call `fsync(2)` for every message -- it may be just saved to cache and not really written to the disk.
"""


"""fair dispatch
By default, RabbitMQ will dispatch the message by its round-robin manner or its odds.
but not all message are equal, some message may take longer time to process. so we need to dispatch the message fairly.
uses `channel.basic_qos(prefetch_count=1)` to ensure the worker only receive one message at a time.
so the not busy worker will receive the message immediately.
"""


cred = pika.credentials.PlainCredentials(username="admin", password="admin")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=cred)
)
channel = connection.channel()


channel.queue_declare(queue="task_queue", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    sleep(body.count(b"."))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue", on_message_callback=callback)

channel.start_consuming()
