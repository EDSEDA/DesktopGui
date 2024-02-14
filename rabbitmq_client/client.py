import pika


class RabbitMQClient:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

    def consume(self):
        def callback(ch, method, properties, body):
            print(f"Received {body}")
            # Обработайте данные здесь и передайте их в GUI.

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
