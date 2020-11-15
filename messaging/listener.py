import os
import sys
import json
from messaging.connection import Connection
from messaging.constants import *


def main():
    channel = Connection().get_channel()
    channel.queue_declare(queue=SIMULATOR_QUEUE)

    def route_message(_ch, _method, _properties, body):
        try:
            body = json.loads(body)
            print("Received message {}".format(body))
            payload_type = body.get("payload_type", None)
            for handler in  HANDLER_MAPPING[payload_type]:
                print("Calling handler {}".format(handler))
                handler(body).call()
        except Exception as e:
            print("Unable to understand received message {}".format(str(e)))

    channel.basic_consume(queue=SIMULATOR_QUEUE, on_message_callback=route_message, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)