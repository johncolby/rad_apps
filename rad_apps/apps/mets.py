from flask_wtf import FlaskForm
from wtforms import BooleanField
from ..appplugin import AppPlugin

class Options(FlaskForm):
    mni_bool = BooleanField('MNI template')

app = AppPlugin(long_name = 'Metastasis', 
             form_opts = Options,
             wrapper_fun = None)