from flask_wtf          import FlaskForm
from wtforms            import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import wtforms_json

wtforms_json.init()


class RegisterForm(FlaskForm):
    sentence = StringField('Sentence:', validators = [DataRequired(), Length(min = 0, max = 100)])
    submit   = SubmitField('Analyse')

