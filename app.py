from flask import Flask, request, render_template, redirect, url_for, flash
from celery import Celery
import os
import brats_preprocessing.brats_preprocessing as bp
from celery.utils.log import get_task_logger

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
logger = get_task_logger(__name__)

url        = 'https://air.radiology.ucsf.edu/api/'
model_path = '/mnt/crypt/jcolby/dcmclass/model.Rdata'
cred_path  = '/home/jcolby/.air_login.txt'
endpoint   = 'http://localhost:8082/predictions/unet'

@celery.task
def sleep_x(secs):
    os.system(f'sleep {secs}')

@celery.task
def cli(acc):
    mri = bp.tumor_study(acc = acc, model_path = model_path)
    logger.info(mri.acc)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('input.html')
    if request.method == 'POST':
        acc = request.form['acc']
        cli.delay(acc)
        return redirect(url_for('main'))