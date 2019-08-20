from flask import Flask, request, render_template, redirect, url_for, flash
import os
import brats_preprocessing.brats_preprocessing as bp
import argparse
from redis import Redis
import rq
from flask_mail import Mail, Message
from dotenv import load_dotenv

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app.config['SECRET_KEY']    = os.environ.get('SECRET_KEY') or '12345678'
app.config['REDIS_URL']     = os.environ.get('REDIS_URL') or 'redis://'
app.config['MAIL_SERVER']   = os.environ.get('MAIL_SERVER') or 'smtp.office365.com'
app.config['MAIL_PORT']     = os.environ.get('MAIL_PORT') or 587
app.config['MAIL_USE_TLS']  = os.environ.get('MAIL_USE_TLS') or 1
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

queue = rq.Queue(connection=Redis.from_url(app.config['REDIS_URL']))

mail = Mail(app)

args = argparse.Namespace()
args.url_air         = 'https://air.radiology.ucsf.edu/api/'
args.model_path      = '/mnt/crypt/jcolby/dcmclass/model.Rdata'
args.cred_path       = '/home/jcolby/.air_login.txt'
args.url_seg         = 'http://localhost:8082/predictions/unet'
args.mni_mask        = True
args.do_bias_correct = True

def send_email(subject, sender, recipients, text_body, html_body = '',
               attachments = None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    mail.send(msg)

def process_gbm_wrapper(args):
    bp.process_gbm(args)
    # os.system('sleep 1')
    report_path = f'{args.acc}_gbm.pdf'
    app.app_context().push()
    with app.open_resource(report_path) as fp:
        send_email(subject = 'secure: glioma segmentation',
                   sender = 'john.colby@ucsf.edu',
                   recipients = [args.email],
                   text_body = f'Accession #: {args.acc}\n\n',
                   attachments = [(report_path, 'application/pdf', fp.read())])
    os.remove(report_path)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('input.html')
    if request.method == 'POST':
        args.acc = request.form['acc']
        args.email = request.form['email']
        queue.enqueue(process_gbm_wrapper, args, job_timeout=2700)
        return redirect(url_for('main'))