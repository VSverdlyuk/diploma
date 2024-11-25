from flask import Flask, render_template, request, redirect, url_for
from models import db, Book
from forms import BookForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # For CSRF protection
db.init_app(app)


@app.route('/')
def book_list():
    """
    Renders the list of all books in the database.

    Returns:
        A rendered template displaying all books.
    """
    books = Book.query.all()
    return render_template('book_list.html', books=books)


@app.route('/book/create', methods=['GET', 'POST'])
def book_create():
    """
    Handles the creation of a new book.

    - On GET request, displays a form for creating a new book.
    - On POST request, validates and saves the new book to the database.

    Returns:
        On success, redirects to the book list.
        Otherwise, re-renders the form with errors.
    """
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            description=form.description.data,
            published_date=form.published_date.data
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('book_list'))
    return render_template('book_form.html', form=form)


@app.route('/book/<int:id>', methods=['GET'])
def book_detail(id):
    """
    Displays detailed information about a specific book.

    Args:
        id (int): The ID of the book to display.

    Returns:
        A rendered template displaying the book's details.
    """
    book = Book.query.get_or_404(id)
    return render_template('book_detail.html', book=book)


@app.route('/book/<int:id>/edit', methods=['GET', 'POST'])
def book_edit(id):
    """
    Handles editing an existing book.

    - On GET request, pre-fills the form with the book's data.
    - On POST request, validates and updates the book in the database.

    Args:
        id (int): The ID of the book to edit.

    Returns:
        On success, redirects to the book list.
        Otherwise, re-renders the form with errors.
    """
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.description = form.description.data
        book.published_date = form.published_date.data
        db.session.commit()
        return redirect(url_for('book_list'))
    return render_template('book_form.html', form=form, book=book)


@app.route('/book/<int:id>/delete', methods=['GET', 'POST'])
def book_delete(id):
    """
    Handles deleting an existing book.

    - On GET request, displays a confirmation page.
    - On POST request, deletes the book from the database.

    Args:
        id (int): The ID of the book to delete.

    Returns:
        On success, redirects to the book list.
        Otherwise, renders the confirmation page.
    """
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('book_list'))
    return render_template('book_confirm_delete.html', book=book)


if __name__ == '__main__':
    """
    Starts the Flask application in debug mode for development purposes.
    """
    app.run(debug=True)
