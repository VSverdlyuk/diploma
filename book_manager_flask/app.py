# python app.py


from flask import Flask, render_template, request, redirect, url_for
from models import db, Book
from forms import BookForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Для работы с CSRF защитой
db.init_app(app)

@app.route('/')
def book_list():
    books = Book.query.all()
    return render_template('book_list.html', books=books)

@app.route('/book/create', methods=['GET', 'POST'])
def book_create():
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
    book = Book.query.get_or_404(id)
    return render_template('book_detail.html', book=book)

@app.route('/book/<int:id>/edit', methods=['GET', 'POST'])
def book_edit(id):
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
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('book_list'))
    return render_template('book_confirm_delete.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)
