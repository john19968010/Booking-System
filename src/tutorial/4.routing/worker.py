import pika
import sys

cred = pika.credentials.PlainCredentials(username="admin", password="admin")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=cred)
)
channel = connection.channel()
channel.exchange_declare(exchange="direct_logs", exchange_type="direct")


result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    # Only bind the queue with the routing_key
    channel.queue_bind(exchange="direct_logs", queue=queue_name, routing_key=severity)

print(" [*] Waiting for logs. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")


# auto_ack=True, so RabbitMQ will delete the message from the queue as soon as it is delivered.
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
