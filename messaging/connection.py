import pika
import os
import yaml


class Connection(object):
    def __init__(self):
        self.connection = None

    @classmethod
    def __get_configs(cls):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'configs', 'rabbitmq.yml')) as file:
            configs = yaml.load(file, Loader=yaml.FullLoader)
            return configs

    def get_channel(self):
        configs = Connection.__get_configs()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(configs['brokers'], configs['port'], '/', pika.PlainCredentials(configs['user'],
                                                                                                      configs['password'])))
        return self.connection.channel()

    def close(self):
        self.connection.close()
