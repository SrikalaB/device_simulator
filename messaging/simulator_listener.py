import os
import sys
from messaging.connection import Connection
from messaging.constants import *


def main():
    channel = Connection().get_channel()
    channel.queue_declare(queue=SIMULATOR_QUEUE)

    def simulator(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue=SIMULATOR_QUEUE, on_message_callback=simulator, auto_ack=True)

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