from flask_wtf import FlaskForm
import os
from urllib.parse import urljoin

from rad_apps.appplugin import AppPlugin
from radstudy import RadStudy

class Options(FlaskForm):
    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(Options, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)

class TestStudy(RadStudy):
    def download(self):
        pass
    def process(self):
        pass
    def report(self):
        report_path = os.path.join(self.dir_tmp, 'output', 'test.pdf')
        with open(report_path, 'w') as fh:
            print(f'Accession: {self.acc}', file=fh)

def wrapper_fun(app, form):
    TestStudy(acc = form['acc'],
              # download_url = app.config['AIR_URL'],
              # cred_path = app.config['DOTENV_FILE'],
              # process_url = urljoin(app.config['SEG_URL'], 'test'),
              output_dir = os.path.join(app.config['OUTPUT_DIR_NODE'], 'test')
              ).run()

app = AppPlugin(long_name = 'Test application',
                short_name = 'test',
           form_opts = Options,
           wrapper_fun = wrapper_fun)
