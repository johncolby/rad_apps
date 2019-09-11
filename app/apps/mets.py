from flask_wtf import FlaskForm
from wtforms import BooleanField
from ..radapp import RadApp

class Options(FlaskForm):
    mni_bool = BooleanField('MNI template')

app = RadApp(long_name = 'Metastasis', 
             form_opts = Options,
             wrapper_fun = None)