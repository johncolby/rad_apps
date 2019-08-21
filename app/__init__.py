from flask import Flask
from config import Config
from redis import Redis
import rq
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

queue = rq.Queue(connection=Redis.from_url(app.config['REDIS_URL']))

mail = Mail(app)

from app import routes