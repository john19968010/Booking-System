import os
import pika
from pika import credentials
from dotenv import load_dotenv
import subprocess

load_dotenv()


class MessageQueue:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        cred = credentials.PlainCredentials(
            username=os.getenv("MQ_ACCOUNT"), password=os.getenv("MQ_PASSWORD")
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.getenv("MQ_HOST"), port=os.getenv("MQ_PORT"), credentials=cred
            )
        )

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.connection.close()

    def declare_queue(self, queue_name: str):
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def publish_message(
        self, body: str = "", routing_key: str = "", exchange: str = ""
    ):
        """
        Args:
            body: the message to send, like a description of the task.
            routing_key: the message key, like a task name.
            ?????exchange: the exchange name.?????
        """
        self.channel.basic_publish(
            exchange=exchange, routing_key=routing_key, body=body
        )

    def consume_message(self, name: str, callback: callable | None = None):
        """
        Args:
            name: the queue name, must matching with message's routing_key.
            callback: the callback function, like a task, if it None, set auto_ack=True.
                auto_ack = True, it immediately delete the message when it delivered.
        """

        if callback is None:
            self.channel.basic_consume(queue=name, auto_ack=True)
        else:
            self.channel.basic_consume(queue=name, on_message_callback=callback)
        self.channel.start_consuming()


class MessageQueueMonitoring:
    def __generate_cmd(self, cmd) -> str:
        """
        Because we run rabbitMQ in a docker container, so we need to run the command in the container.
        """
        return f'docker exec {os.getenv("CONTAINER NAME")} {cmd}'

    def list_unack_messages(self):
        cmd = self.__generate_cmd(
            "rabbitmqctl list_queues name messages_ready messages_unacknowledged"
        )
        try:
            sub = subprocess.run(cmd, shell=True, check=True, capture_output=True)
            stdout = sub.stdout.decode("utf-8")
            """
            'Timeout: 60.0 seconds ...\nListing queues for vhost / ...\nname\tmessages_ready\tmessages_unacknowledged\nhello3\t0\t0\nhello\t0\t0\n'
            """
        except subprocess.CalledProcessError as e:
            print(e)
            if e.returncode == 127:
                print("please install rabbitmqctl before use this system")

    def run_cmd(
        self,
        cmd: str,
        *,
        shell: bool = True,
        check: bool = True,
        capture_output: bool = True,
    ):
        """
        Args:
            shell: If true, the command will be executed through the shell(Able to use shell feature, such pipe.)
            check: If true, raise a CalledProcessError if the process return code is non-zero, otherwise it needs to check return code by yourself.
            capture_output: If true, stdout and stderr will be captured.
        """
        pass
        # if check:
        #     try:

        #     except subprocess.CalledProcessError:

        # return subprocess.run(cmd, shell=shell, check=check, capture_output=capture_output)
