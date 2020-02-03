import os
from flask import Flask
from .config import Defaults
from redis import Redis
import rq
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from .radapps import RadApps
from dotenv import dotenv_values

app = Flask(__name__)

app.config.from_object(Defaults)
app.config['DOTENV_FILE'] = os.environ.get('DOTENV_FILE') or '.env'
app.config.update(dotenv_values(app.config['DOTENV_FILE']))

queue = rq.Queue(connection=Redis.from_url(app.config['REDIS_URL']))

mail = Mail(app)

bootstrap = Bootstrap(app)

app_list = RadApps()

from rad_apps import routes