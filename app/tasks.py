import os
import argparse
import brats_preprocessing.brats_preprocessing as bp
from app import app
from app.email import send_email

def process_gbm_wrapper(form):
    args = argparse.Namespace()
    args.acc             = form['acc']
    args.url_air         = 'https://air.radiology.ucsf.edu/api/'
    args.model_path      = '/mnt/crypt/jcolby/dcmclass/model.Rdata'
    args.cred_path       = '/home/jcolby/.air_login.txt'
    args.url_seg         = 'http://localhost:8082/predictions/unet'
    args.mni_mask        = True
    args.do_bias_correct = True

    bp.process_gbm(args)
    report_path = f'{args.acc}_gbm.pdf'
    app.app_context().push()
    with app.open_resource(os.path.join('..', report_path)) as fp:
        send_email(subject = 'secure: glioma segmentation',
                   sender = 'john.colby@ucsf.edu',
                   recipients = [form['email']],
                   text_body = f'Accession #: {args.acc}\n\n',
                   attachments = [(report_path, 'application/pdf', fp.read())])
    os.remove(report_path)