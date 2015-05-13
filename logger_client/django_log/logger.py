import uuid

import kombu

from . import settings
from .producer import BlockingProducer


connection = kombu.Connection(
    hostname=settings.BROKER_HOST,
    port=settings.BROKER_PORT,
    userid=settings.BROKER_USERNAME,
    password=settings.BROKER_PASSWORD,
    virtual_host=settings.BROKER_VIRTUAL_HOST,
)
connection.connect()

producer = BlockingProducer(
    connection=connection,
    group_id=settings.GROUP_ID,
    exchange_name=settings.EXCHANGE_NAME,
    exchange_type=settings.EXCHANGE_TYPE,
    queue_name=settings.QUEUE_NAME,
    routing_key=settings.ROUTING_KEY
)


def start(path, username=None, data=None, label=None, user_request_id=None):
    user_request_id = user_request_id or uuid.uuid4().hex
    log(user_request_id=user_request_id, data=data, path=path, label=label, username=username)
    return user_request_id


def log(user_request_id, data, path=None, label=None, username=None):
    # TODO: add group_id!!!
    producer.send_message(user_request_id, data, label=label, path=path, username=username)
