
## Introduction
This tutorial is focus on working subscribe on specific groups of message e.g Two queues, one is to writing `warning` logger in file, the other it get logger from all level

- Setting exchange type as `direct`, so the message goes to the queue which is bound with the routing_key.


## Q&A

Q. what is `routing_key`?  
A. Routing key is used to binding between queues and the exchange, just like letter's address, routing_key tell which queue(s) should receive the message. However it only works on certain exchange type e.g. `direct`, some of it does not works e.g `fanout`, `topic`


