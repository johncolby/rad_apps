import argparse
from flask_wtf import FlaskForm
from wtforms import BooleanField, FormField, IntegerField
from wtforms.validators import Optional
import brats_preprocessing.brats_preprocessing as bp
from ..radapp import RadApp

class Inputs(FlaskForm):
    flair = IntegerField('FLAIR', validators=[Optional()])
    t1 = IntegerField('T1', validators=[Optional()])
    t1ce = IntegerField('T1CE', validators=[Optional()])
    t2 = IntegerField('T2', validators=[Optional()])
    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(Inputs, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs) 

class Options(FlaskForm):
    mni_mask = BooleanField('MNI template')
    bias_correct = BooleanField('Bias field correct')
    inputs = FormField(Inputs)
    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(Options, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)

def wrapper_fun(app, form, output_dir):
    args = argparse.Namespace()
    args.acc             = form['acc']
    args.air_url         = app.config['AIR_URL']
    args.model_path      = app.config['MODEL_RDATA']
    args.cred_path       = app.config['DOTENV_FILE']
    args.seg_url         = app.config['SEG_URL']
    args.mni_mask        = form['opts']['mni_mask']
    args.do_bias_correct = form['opts']['bias_correct']
    args.output_dir      = output_dir

    bp.process_gbm(args)


app = RadApp(long_name = 'Glioblastoma', 
           form_opts = Options,
           wrapper_fun = wrapper_fun)