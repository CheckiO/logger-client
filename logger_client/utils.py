class AMQPDataWrapper(object):

    def __init__(self, data, user_request_id):
        self.data = data
        self.user_request_id = user_request_id

    def encode(self):
        return {
            'data': self.data,
            'user_request_id': self.user_request_id,
        }

    @classmethod
    def decode(cls, message):
        return cls(message.get('data'), message.get('user_request_id'))

    @staticmethod
    def is_wrapped(message):
        return 'user_request_id' in message and 'data' in message
