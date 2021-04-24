from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddDepartmentForm(FlaskForm):
    title = StringField("Department Title", validators=[DataRequired()])
    chief = IntegerField('Chief id', validators=[DataRequired()])
    members = StringField("Collaborators", validators=[DataRequired()])
    email = EmailField("Department Email", validators=[DataRequired()])
    submit = SubmitField('Add')
