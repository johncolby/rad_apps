import os


class Defaults(object):
    APPS = "['testapp']"
    SECRET_KEY = '12345678'
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MODEL_RDATA = 'model.Rdata'
    OUTPUT_DIR_NODE = '.'
