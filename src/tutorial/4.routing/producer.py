import pika
import pika.credentials
import sys


cred = pika.credentials.PlainCredentials(username="admin", password="admin")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=cred)
)
channel = connection.channel()
# TODO: what is direct in exchange_type?
"""
Declare exchange with exchange_type `direct`, 
so when 
message(routing_key) goes to the queue which is bound with the routing_key
"""

channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

"""
severity: in this case, it is used to declared the level of log message,
    setting it as routing_key, so the message will be sent to the queue which is bound with the routing_key
"""
severity = sys.argv[1] if len(sys.argv) > 1 else "info"
message = " ".join(sys.argv[2:]) or "Hello World!"

# TODO: what is routing_key used for?
channel.basic_publish(exchange="direct_logs", routing_key=severity, body=message)
print(f" [x] Sent {severity}:{message}")
connection.close()
