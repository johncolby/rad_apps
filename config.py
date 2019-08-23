import os
from dotenv import load_dotenv

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))

    SECRET_KEY    = os.environ.get('SECRET_KEY') or '12345678'
    REDIS_URL     = os.environ.get('REDIS_URL') or 'redis://'
    MAIL_SERVER   = os.environ.get('MAIL_SERVER') or 'smtp.office365.com'
    MAIL_PORT     = os.environ.get('MAIL_PORT') or 587
    MAIL_USE_TLS  = os.environ.get('MAIL_USE_TLS') or 1
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')