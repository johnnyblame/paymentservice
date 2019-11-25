from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired

CURRENCY_CHOICES = [(978, 'EUR'), (840, 'USD'), (643, 'RUB')]


class PayForm(FlaskForm):
    amount = StringField('Amount', validators=[DataRequired()])
    currency = SelectField('Currency', choices=CURRENCY_CHOICES)
    product_info = TextAreaField('Product Info')
    submit = SubmitField("Pay")
