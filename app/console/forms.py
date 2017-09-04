from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required, Length


class APIKeyForm(FlaskForm):
    application = StringField('Application Name',
                              validators=[Required(), Length(0, 64)])
    description = TextAreaField('Description')
    submit = SubmitField('Create API Key')
