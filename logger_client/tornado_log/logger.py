import uuid


from .producer import TornadoProducer


class TornadoRequestLogger(object):

    def __init__(self, exchange_name=None, exchange_type=None, queue_name=None, routing_key=None):
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.queue_name = queue_name
        self.routing_key = routing_key

        self.producer = None
        self.channel = None

    def set_channel(self, channel):
        self.channel = channel
        self.producer = TornadoProducer(
            channel=self.channel,
            exchange_name=self.exchange_name,
            exchange_type=self.exchange_type,
            queue_name=self.queue_name,
            routing_key=self.routing_key
        )

    def start(self, path, username=None, data=None, label=None, user_request_id=None):
        user_request_id = user_request_id or uuid.uuid4().hex
        self.producer.send_message(user_request_id, data, label=label, path=path, username=username)
        return user_request_id

    def log(self, user_request_id, data, label=None, username=None):
        self.producer.send_message(user_request_id, data, label=label, username=username)
