import os
from app import app, rad_apps
from app.email import send_email

def app_wrapper(app_name, form):
    rad_app = rad_apps.apps[app_name]
    output_dir = os.path.join(app.config['OUTPUT_DIR_NODE'], app_name)
    rad_app.wrapper_fun(app, form, output_dir)

    report_name = f'{form["acc"]}_{app_name}.pdf'
    report_path = os.path.join(output_dir, form["acc"], f'{app_name}.pdf')
    app.app_context().push()
    with open(os.path.join(report_path), 'rb') as fp:
        send_email(subject = f'secure: {rad_app.long_name} analysis report',
                   sender = app.config['MAIL_USERNAME'],
                   recipients = [form['email']],
                   text_body = f'Accession #: {form["acc"]}\n\n',
                   attachments = [(report_name, 'application/pdf', fp.read())])