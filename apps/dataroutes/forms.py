from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


# Subscription Request
class CreateSubscriptionRequestForm(FlaskForm):
    data_requested_id = StringField('Datastack ID', id='datastack_id', validators=[DataRequired(), Length(max=64)])
    identity_document = FileField('Identity document', id='identity_document', validators=[DataRequired()])
    authority_document = FileField('Authority document', id='authority_document', validators=[DataRequired()])
    purpose = TextAreaField('Purpose', id='purpose', validators=[DataRequired()])

