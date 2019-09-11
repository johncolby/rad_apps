import os
from app import app, rad_apps
from app.email import send_email

def app_wrapper(app_name, form):
    rad_app = rad_apps.apps[app_name]
    
    rad_app.wrapper_fun(app, form)

    report_path = f'{form["acc"]}_gbm.pdf'
    app.app_context().push()
    with open(os.path.join(report_path), 'rb') as fp:
        send_email(subject = f'secure: {rad_app.long_name} analysis report',
                   sender = app.config['MAIL_USERNAME'],
                   recipients = [form['email']],
                   text_body = f'Accession #: {form["acc"]}\n\n',
                   attachments = [(report_path, 'application/pdf', fp.read())])
    os.remove(report_path)
