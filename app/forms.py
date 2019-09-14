from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField, SelectField, FormField, SubmitField
from wtforms.validators import Optional, DataRequired, Email, Length, Regexp
from app import app, rad_apps

class ChooseApp(FlaskForm):
    app_name = SelectField('Application', choices=rad_apps.get_app_list())
    submit = SubmitField('Submit') 

def get_form(app_name):
    with app.app_context():
        class SegmentationForm(FlaskForm):
            acc = StringField('Accession Number', 
                              render_kw={"placeholder": "12345678"}, 
                              validators=[DataRequired(), 
                                          Length(min = 8, max = 8), 
                                          Regexp('[0-9]{8}')])
            email = StringField('Email', validators=[Optional(), Email()])
            opts = FormField(rad_apps.apps[app_name].form_opts)
            submit = SubmitField('Submit')
        return SegmentationForm()