
## Introduction
This tutorial is focus on enhancing the previous tutor, we want to subscribe not only based on routing key, but also base on the content we send.
 
- Setting exchange type as `topic`, and using the following code to find the matching content
    - `*`(substitute for exactly one word.)
    - `#` (substitute for zero or more words.)


## Q&A

Q. what is `routing_key`?  
A. Routing key is used to binding between queues and the exchange, just like letter's address, routing_key tell which queue(s) should receive the message. However it only works on certain exchange type e.g. `direct`, some of it does not works e.g `fanout`, `topic`


