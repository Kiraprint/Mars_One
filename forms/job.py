from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    title = StringField("Job Title", validators=[DataRequired()])
    team_lead = IntegerField('Team Leader id', validators=[DataRequired()])
    size = IntegerField('Work Size', validators=[DataRequired()])
    collaborators = StringField("Collaborators", validators=[DataRequired()])
    finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')
