from messaging.connection import Connection


class MessageProducer(object):

    __instance = None

    def __init__(self):
        """
        Constructor to instantiate the MessageProducer
        This method will throw an Exception if it is called after a singleton instance of this object
        already exists
        """
        if MessageProducer.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.channel = Connection().get_channel()
            MessageProducer.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to return a singleton instance of this class
        :param entity: str representing the entity
        """
        if MessageProducer.__instance is None:
            MessageProducer()
        return MessageProducer.__instance

    def publish(self, message, exchange="", routing_key="", queue=None):
        try:
            if queue:
                self.channel.queue_declare(queue=queue)
            self.channel.basic_publish(body=message, exchange=exchange, routing_key=queue)
        except:
            print("Unable to publish messages")
            raise
