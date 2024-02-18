
## Introduction
This tutorial is to send task to all workers, it is useful to use on logging system

## Q&A

Q. what is `exchage`?   
A. exchange is the communication between queue and producer 
and know what exactly what to do next. e,g, discard it / append to multi queue / append to one queue

if exchange is not set, the message will be sent to  default or nameless exchange, 
task will send to the queue with the same name as routing_key(if exists).
