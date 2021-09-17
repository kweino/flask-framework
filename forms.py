from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length

class StockForm(FlaskForm):
    ticker = StringField('Stock Ticker Symbol', validators=[DataRequired()])
    ticker_date = DateField('Desired Date', validators=[DataRequired()], format='%Y-%m')
    submit = SubmitField('Find a New Stock!')
