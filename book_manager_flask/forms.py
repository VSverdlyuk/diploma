from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    """
    A form for creating and editing books in the library.

    Fields:
        title (StringField): The title of the book (required).
        author (StringField): The author of the book (required).
        description (TextAreaField): A brief description of the book (optional).
        published_date (DateField): The date the book was published (required).
    """
    title = StringField(
        'Title',
        validators=[DataRequired()],
        description="Enter the book's title."
    )
    author = StringField(
        'Author',
        validators=[DataRequired()],
        description="Enter the author's name."
    )
    description = TextAreaField(
        'Description',
        description="Provide a brief description of the book."
    )
    published_date = DateField(
        'Published Date',
        format='%Y-%m-%d',
        validators=[DataRequired()],
        description="Enter the published date in YYYY-MM-DD format."
    )
