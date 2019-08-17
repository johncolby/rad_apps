from flask import Flask, request, render_template, redirect, url_for, flash
from celery import Celery
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def sleep_x(secs):
    os.system(f'sleep {secs}')

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('input.html')
    if request.method == 'POST':
        acc = request.form['acc']
        sleep_x.delay(acc)
        return redirect(url_for('main'))