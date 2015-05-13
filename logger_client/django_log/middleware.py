from threading import current_thread

from . import logger


class GlobalRequestId(object):
    _request_ids = {}

    @staticmethod
    def get_request_id():
        try:
            return GlobalRequestId._request_ids[current_thread()]
        except KeyError:
            return None

    def process_request(self, request):
        user_request_id = self.start_logging(request)
        GlobalRequestId._request_ids[current_thread()] = user_request_id

    def process_response(self, request, response):
        # Cleanup
        thread = current_thread()
        try:
            del GlobalRequestId._request_ids[thread]
        except KeyError:
            pass
        return response

    def _get_username(self, request):
        return request.user.username

    def start_logging(self, request, data=None):
        username = self._get_username(request)
        return logger.start(path=request.path, username=username, data=data, label="django: start")


def log_request(data, label=None, username=None):
    user_request_id = GlobalRequestId.get_request_id()
    logger.log(user_request_id, data, label=label, username=username)
