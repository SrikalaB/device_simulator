from messaging.connection import Connection

class MessageProducer(object):
    def __init__(self):
        self.channel = None

    def publish(self, message, exchange="", routing_key="", queue=None):
        try:
            if not self.channel:
                self.channel = Connection().get_channel()
            if queue:
                self.channel.queue_declare(queue=queue)
            self.channel.basic_publish(
                body=message,
                exchange=exchange,
                routing_key=queue
            )
            Connection().close
        except:
            print("Unable to publish messages")
            raise
