import pika
import pika.credentials
import sys


cred = pika.credentials.PlainCredentials(username="admin", password="admin")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=cred)
)
channel = connection.channel()
"""
Declare exchange with exchange_type `direct`, 
so when 
message(routing_key) goes to the queue which is bound with the routing_key
"""

channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

"""
severity: in this case, it is used to declared the level of log message,
    setting it as routing_key, so the message will be sent to the queue which is bound with the routing_key
"""
routing_key = sys.argv[1] if len(sys.argv) > 2 else "anonymous.info"
message = " ".join(sys.argv[2:]) or "Hello World!"

channel.basic_publish(exchange="topic_logs", routing_key=routing_key, body=message)
print(f" [x] Sent {routing_key}:{message}")
connection.close()
