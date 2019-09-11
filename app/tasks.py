import os
import argparse
import brats_preprocessing.brats_preprocessing as bp
from app import app
from app.email import send_email

def process_gbm_wrapper(form):
    args = argparse.Namespace()
    args.acc             = form['acc']
    args.air_url         = app.config['AIR_URL']
    args.model_path      = app.config['MODEL_RDATA']
    args.cred_path       = None
    args.seg_url         = app.config['SEG_URL']
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