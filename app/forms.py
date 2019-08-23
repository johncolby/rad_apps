from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class SegmentationForm(FlaskForm):
    acc = StringField('Accession Number', validators=[DataRequired(), 
                                                      Length(min = 8, max = 8), 
                                                      Regexp('[0-9]{8}')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')