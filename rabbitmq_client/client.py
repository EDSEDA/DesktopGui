import logging
from threading import Thread

import pika

from config import settings

logging.basicConfig(level=logging.INFO)


class RabbitMQClient:
    def __init__(self, gui_queue, queue_name=settings.QUEUE_NAME):
        self.queue_name = queue_name
        self.gui_queue = gui_queue
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                credentials=pika.PlainCredentials(
                    settings.RABBITMQ_USER,
                    settings.RABBITMQ_PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()

        # Declare the queue in case it doesn't already exist
        self.channel.queue_declare(queue=self.queue_name)

    def consume(self):
        def callback(ch, method, properties, body):
            logging.info(f"Received: {body}")
            # Put the message body into the queue for the GUI to process
            self.gui_queue.put(body)

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            self.connection.close()
            logging.info("RabbitMQ connection closed.")

    def start_consuming(self):
        # Run the consume method in a separate thread
        Thread(target=self.consume, daemon=True).start()
