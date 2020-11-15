import pika
import yaml
import os


class MessageProducer(object):
    def __init__(self):
        self.channel = None

    @classmethod
    def __get_configs(cls):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'configs', 'rabbitmq.yml')) as file:
            configs = yaml.load(file, Loader=yaml.FullLoader)
            return configs

    def __connection(self):
        configs = MessageProducer.__get_configs()
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(configs['brokers'], configs['port'], '/', pika.PlainCredentials(configs['user'],
                                                                                                      configs['password'])))
        return connection.channel()

    def publish(self, message, exchange="", routing_key=""):
        try:
            if not self.channel:
                self.channel = self.__connection()
            self.channel.basic_publish(
                body=message,
                exchange=exchange,
                routing_key=routing_key
            )
        except:
            raise
