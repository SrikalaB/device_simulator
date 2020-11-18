import sys
import os
import pika
import yaml
from utils import on_error_retry


class Connection(object):

    @classmethod
    def __get_configs(cls, from_config_file=False):
        if from_config_file:
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'configs',
                                   'rabbitmq.yml')) as file:
                configs = yaml.load(file, Loader=yaml.FullLoader)
                return configs
        else:
            user = os.getenv("USER", None)
            password = os.getenv("PASSWORD", None)
            if user is None or password is None:
                print("[ERROR] Set env variables USER and PASSWORD to hold auth credentials to RabbitMQ")
                sys.exit(1)
            return {"brokers": os.getenv('BROKERS', "rabbitmq"),
                    "port": os.getenv('PORT', "5672"),
                    "user": user,
                    "password": password}

    @on_error_retry
    def get_channel(self):
        try:
            configs = Connection.__get_configs()
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(configs['brokers'], configs['port'], '/', pika.PlainCredentials(configs['user'],
                                                                                                          configs['password'])))
            if connection is None:
                raise Exception("Unable to establish connection to RabbitMQ")
            return connection.channel()
        except Exception as e:
            print("[ERROR] Unable to connect to RabbitMQ. Retrying...")
            raise Exception("[ERROR] Unable to connect to RabbitMQ")

    def close(self, connection):
        connection.close()
