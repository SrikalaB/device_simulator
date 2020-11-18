import pika
import os
import yaml


class Connection(object):
    def __init__(self):
        self.connection = None

    @classmethod
    def __get_configs(cls, from_config_file=True):
        if from_config_file:
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'configs',
                                   'rabbitmq.yml')) as file:
                configs = yaml.load(file, Loader=yaml.FullLoader)
                return configs
        else:
            return {"brokers": os.getenv('BROKERS', "127.0.0.1"),
                    "port": os.getenv('PORT', "5672"),
                    "user": os.getenv("USER", None),
                    "password": os.getenv("PASSWORD", None)}

    def get_channel(self):
        try:
            configs = Connection.__get_configs()
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(configs['brokers'], configs['port'], '/', pika.PlainCredentials(configs['user'],
                                                                                                          configs['password'])))
            if self.connection is None:
                raise Exception("Unable to establish connection to RabbitMQ")
            return self.connection.channel()
        except Exception as e:
            raise Exception("Unable to connect to RabbitMQ")

    def close(self):
        self.connection.close()
