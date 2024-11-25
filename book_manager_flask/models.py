from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    """
    Represents a book in the library database.

    Attributes:
        id (int): The unique identifier for the book.
        title (str): The title of the book (required, max 150 characters).
        author (str): The author of the book (required, max 100 characters).
        description (str): A brief description of the book (optional).
        published_date (date): The publication date of the book (optional).
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    published_date = db.Column(db.Date)

    def __repr__(self):
        """
        Returns a string representation of the Book instance.

        Returns:
            str: A string containing the book's title.
        """
        return f"<Book {self.title}>"
