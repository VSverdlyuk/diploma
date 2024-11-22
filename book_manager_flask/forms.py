from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    description = TextAreaField('Description')
    published_date = DateField('Published Date', format='%Y-%m-%d', validators=[DataRequired()])
