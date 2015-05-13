import json
from functools import partial

from django.utils.timezone import now
from kombu import Exchange, Queue, Producer
from kombu.serialization import registry

from .utils import JSONEncoder


class BlockingProducer(object):

    def __init__(self, connection, group_id, exchange_name, exchange_type, queue_name,
                 routing_key):
        self.channel = connection.channel()
        self.group_id = group_id
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.queue_name = queue_name
        self.routing_key = routing_key

        self.producer = None
        self.queue = None
        self.exchange = None
        self.init_queue()

    def init_queue(self):
        self.exchange = Exchange(name=self.exchange_name, type=self.exchange_type,
                                 channel=self.channel)
        self.exchange.durable = False
        self.exchange.declare()

        self.queue = Queue(name=self.queue_name, exchange=self.exchange,
                           routing_key=self.routing_key, channel=self.channel)
        self.queue.durable = False
        self.queue.declare()

        self.producer = Producer(channel=self.channel, exchange=self.exchange, serializer='json')

    def send_message(self, user_request_id, data, label=None, path=None, username=None):
        message = {
            'user_request_id': user_request_id,
            'created_at': now().isoformat(),
            'data': data,
            'label': label,
            'path': path,
            'username': username,
        }
        self.producer.publish(message, routing_key=self.routing_key)


def register_json():
    json_dumps = partial(json.dumps, cls=JSONEncoder)
    registry.register('json', json_dumps, None, content_type='application/json',
                      content_encoding='utf-8')
register_json()