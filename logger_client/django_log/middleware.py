from threading import current_thread

from . import logger


class GlobalRequestLogger(object):
    _request_loggers = {}

    def process_request(self, request):
        request_logger = logger.RequestLogger()
        GlobalRequestLogger._request_loggers[current_thread()] = request_logger

        username = self._get_username(request)
        request_logger.start(path=request.path, username=username, label="DJANGO:: start")

    def process_response(self, request, response):
        # Cleanup
        thread = current_thread()
        request_logger = GlobalRequestLogger._request_loggers.get(thread)
        if request_logger is not None:
            request_logger.stop()
            del GlobalRequestLogger._request_loggers[thread]
        return response

    def _get_username(self, request):
        return request.user.username

    @staticmethod
    def get_request_id():
        request_logger = GlobalRequestLogger.get_request_logger()
        if request_logger is not None:
            return request_logger.user_request_id

    @staticmethod
    def get_request_logger():
        try:
            return GlobalRequestLogger._request_loggers[current_thread()]
        except KeyError:
            return None

    @staticmethod
    def log(data, label=None, username=None):
        request_logger = GlobalRequestLogger.get_request_logger()
        if request_logger is not None:
            request_logger.log(data, label=label, username=username)
