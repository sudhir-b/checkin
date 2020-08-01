from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    name = StringField('Name of person', validators=[DataRequired()])
    device_name = StringField('Name of this device', validators=[DataRequired()])
    submit = SubmitField('Register current device with user')