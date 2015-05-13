import json
from datetime import datetime

import pika
import pytz


class TornadoProducer(object):

    EXCHANGE_NAME = 'RequestLogger.E.Direct.Logs'
    EXCHANGE_TYPE = 'direct'
    QUEUE_NAME = 'RequestLogger.Q.PROD.Logs'
    ROUTING_KEY = 'RequestLogger.Q.PROD.Logs'

    def __init__(self, channel, exchange_name=None, exchange_type=None, queue_name=None,
                 routing_key=None):
        self.channel = channel
        self.exchange_name = exchange_name or self.EXCHANGE_NAME
        self.exchange_type = exchange_type or self.EXCHANGE_TYPE
        self.queue_name = queue_name or self.QUEUE_NAME
        self.routing_key = routing_key or self.ROUTING_KEY

        self.properties = pika.BasicProperties(content_type='application/json')

    def init(self):
        self.exchange_declare()

    def exchange_declare(self):
        callback = self.queue_declare if self.EXCHANGE_NAME else None
        self.channel.exchange_declare(exchange=self.EXCHANGE_NAME, type=self.EXCHANGE_TYPE,
                                      callback=callback)

    def queue_declare(self, method_frame):
        self.channel.queue_declare(queue=self.QUEUE_NAME, callback=self.queue_bind)

    def queue_bind(self, method_frame):
        self.channel.queue_bind(callback=self._on_queue_bind, queue=self.QUEUE_NAME,
                                exchange=self.EXCHANGE_NAME, routing_key=self.ROUTING_KEY)

    def _on_queue_bind(self, method_frame):
        pass

    def send_message(self, user_request_id, data, label=None, path=None, username=None):
        message = {
            'user_request_id': user_request_id,
            'created_at': datetime.utcnow().replace(tzinfo=pytz.utc).isoformat(),
            'data': data,
            'label': label,
            'path': path,
            'username': username,
        }

        body = self._encode_body(message)
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=body,
            properties=self.properties
        )

    def _encode_body(self, body):
        return json.dumps(body)
