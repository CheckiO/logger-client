import uuid

import kombu

from . import settings
from .producer import BlockingProducer


class RequestLogger(object):

    def __init__(self):
        self._connection = self._init_connection()
        self._producer = self._init_producer(self._connection)
        self.user_request_id = None

    @staticmethod
    def _init_connection():
        amqp_connection = kombu.Connection(
            hostname=settings.BROKER_HOST,
            port=settings.BROKER_PORT,
            userid=settings.BROKER_USERNAME,
            password=settings.BROKER_PASSWORD,
            virtual_host=settings.BROKER_VIRTUAL_HOST,
        )
        amqp_connection.connect()
        return amqp_connection

    @staticmethod
    def _init_producer(connection):
        return BlockingProducer(
            connection=connection,
            group_id=settings.GROUP_ID,
            exchange_name=settings.EXCHANGE_NAME,
            exchange_type=settings.EXCHANGE_TYPE,
            queue_name=settings.QUEUE_NAME,
            routing_key=settings.ROUTING_KEY
        )

    def start(self, path, username=None, data=None, label=None, user_request_id=None):
        self.user_request_id = user_request_id or uuid.uuid4().hex
        self.log(data=data, path=path, label=label, username=username)
        return self.user_request_id

    def log(self, data, path=None, label=None, username=None):
        # TODO: add group_id!!!
        self._producer.send_message(self.user_request_id, data, label=label, path=path,
                                    username=username)

    def stop(self):
        self._connection.close()
