from flask import Flask, request, render_template, redirect, url_for, flash
from celery import Celery
import os
import brats_preprocessing.brats_preprocessing as bp
from celery.utils.log import get_task_logger
import argparse

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
logger = get_task_logger(__name__)

args = argparse.Namespace()
args.url_air         = 'https://air.radiology.ucsf.edu/api/'
args.model_path      = '/mnt/crypt/jcolby/dcmclass/model.Rdata'
args.cred_path       = '/home/jcolby/.air_login.txt'
args.url_seg         = 'http://localhost:8082/predictions/unet'
args.mni_mask        = True
args.do_bias_correct = False

@celery.task
def cli(acc):
    args.acc = acc
    bp.process_gbm(args)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('input.html')
    if request.method == 'POST':
        acc = request.form['acc']
        cli.delay(acc)
        return redirect(url_for('main'))