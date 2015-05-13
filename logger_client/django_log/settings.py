from django.conf import settings


BROKER_USERNAME = getattr(settings, 'REQUEST_LOGGER_BROKER_USERNAME', 'guest')
BROKER_PASSWORD = getattr(settings, 'REQUEST_LOGGER_BROKER_PASSWORD', 'guest')
BROKER_HOST = getattr(settings, 'REQUEST_LOGGER_BROKER_HOST', 'localhost')
BROKER_PORT = getattr(settings, 'REQUEST_LOGGER_BROKER_PORT', 5672)
BROKER_VIRTUAL_HOST = getattr(settings, 'REQUEST_LOGGER_BROKER_VIRTUAL_HOST', '/')

EXCHANGE_NAME = getattr(settings, 'REQUEST_LOGGER_EXCHANGE_NAME', 'RequestLogger.E.Direct.Logs')
EXCHANGE_TYPE = getattr(settings, 'REQUEST_LOGGER_EXCHANGE_TYPE', 'direct')
QUEUE_NAME = getattr(settings, 'REQUEST_LOGGER_QUEUE_NAME', 'RequestLogger.Q.PROD.Logs')
ROUTING_KEY = getattr(settings, 'REQUEST_LOGGER_ROUTING_KEY', 'RequestLogger.Q.PROD.Logs')

GROUP_ID = getattr(settings, 'REQUEST_LOGGER_GROUP_ID', None)  # grouping service (prod/test)
