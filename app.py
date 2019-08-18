from flask import Flask, request, render_template, redirect, url_for, flash
from celery import Celery
import os
import brats_preprocessing.brats_preprocessing as bp
import argparse
from redis import Redis
import rq

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'

queue = rq.Queue('brats', connection=Redis.from_url('redis://'))

args = argparse.Namespace()
args.url_air         = 'https://air.radiology.ucsf.edu/api/'
args.model_path      = '/mnt/crypt/jcolby/dcmclass/model.Rdata'
args.cred_path       = '/home/jcolby/.air_login.txt'
args.url_seg         = 'http://localhost:8082/predictions/unet'
args.mni_mask        = True
args.do_bias_correct = False

def cli(acc):
    args.acc = acc
    bp.process_gbm(args)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('input.html')
    if request.method == 'POST':
        acc = request.form['acc']
        queue.enqueue('app.cli', acc, job_timeout=2700)
        return redirect(url_for('main'))