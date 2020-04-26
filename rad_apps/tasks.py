import os
from rad_apps import app, app_list
from .email import send_email

def app_wrapper(app_name, form):
    rad_app = app_list.apps[app_name]
    rad_app.wrapper_fun(app, form)

    if form['email']:
        report_name = f'{form["acc"]}_{app_name}.pdf'
        output_dir = os.path.join(app.config['OUTPUT_DIR_NODE'], app_name)
        report_path = os.path.join(output_dir, form["acc"], f'{app_name}.pdf')
        app.app_context().push()
        with open(os.path.join(report_path), 'rb') as fp:
            send_email(subject = f'secure: {rad_app.long_name} analysis report',
                       sender = app.config['MAIL_USERNAME'],
                       recipients = [form['email']],
                       text_body = f'Accession #: {form["acc"]}\n\n',
                       attachments = [(report_name, 'application/pdf', fp.read())])