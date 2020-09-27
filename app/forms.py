from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    FieldList,
    FormField,
    BooleanField,
    HiddenField,
)
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    name = StringField("Name of person", validators=[DataRequired()])
    device_name = StringField("Name of this device", validators=[DataRequired()])
    submit = SubmitField("Register current device with user")


class UnregisterFormRow(FlaskForm):
    select = BooleanField("select")
    device_id = HiddenField("device_id")


class UnregisterForm(FlaskForm):
    rows = FieldList(FormField(UnregisterFormRow))
    submit = SubmitField("Unregister")
