
## acknowledgement
In the previous tutorial, we wrote a program that sends a single message. and set auto_ack=True, 
but this one, we set a proper acknowledgment from the worker by adding `ch.basic_ack(delivery_tag=method.delivery_tag)`, 
in the callback function. to ensure that the task will not lost. However, it only available in the same channel. 


## Message durability
So the `ch.basic_ack(delivery_tag=method.delivery_tag)` can prevent the message lost, but what if the RabbitMQ server is terminated?
We needs two do two things, firstly setting durable on the queue. `channel.queue_declare(queue='hello', durable=True)` , and then 
setting persistent on the message. `channel.basic_publish(exchange='', routing_key='hello', body=message, properties=pika.BasicProperties(
    delivery_mode = pika.DeliveryMode.Persistent))`
NOTE: RabbitMQ doesn't call `fsync(2)` for every message -- it may be just saved to cache and not really written to the disk.



## fair dispatch
By default, RabbitMQ will dispatch the message by its round-robin manner or its odds.
but not all message are equal, some message may take longer time to process. so we need to dispatch the message fairly.
uses `channel.basic_qos(prefetch_count=1)` to ensure the worker only receive one message at a time.
so the not busy worker will receive the message immediately.

