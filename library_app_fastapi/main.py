from fastapi import FastAPI, Form, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import logging

# Database setup
DATABASE_URL = "sqlite:///./library.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create FastAPI app instance
app = FastAPI()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Models
class Book(Base):
    """
    Represents a book in the library database.

    Attributes:
        id (int): The unique identifier for the book.
        title (str): The title of the book.
        author (str): The author's name.
        description (str): A brief description of the book.
        published_date (datetime.date): The publication date of the book.
    """
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    description = Column(String)
    published_date = Column(Date)


# Create tables in the database
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    """
    Dependency to provide a database session.
    Ensures the session is properly closed after use.

    Yields:
        Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Routes
@app.get("/", response_class=HTMLResponse)
async def book_list(request: Request, db: Session = Depends(get_db)):
    """
    Renders a list of all books in the library.

    Args:
        request (Request): The HTTP request object.
        db (Session): The database session.

    Returns:
        HTMLResponse: The rendered HTML response containing the book list.
    """
    books = db.query(Book).all()
    return templates.TemplateResponse("book_list.html", {"request": request, "books": books})


@app.get("/book/new", response_class=HTMLResponse)
async def book_create_form(request: Request):
    """
    Displays the form to create a new book.

    Args:
        request (Request): The HTTP request object.

    Returns:
        HTMLResponse: The rendered HTML response with the book form.
    """
    return templates.TemplateResponse("book_form.html", {"request": request, "book": None})


@app.post("/book/new", response_class=HTMLResponse)
async def book_create(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    published_date: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Handles creating a new book.

    Args:
        request (Request): The HTTP request object.
        title (str): The title of the book.
        author (str): The author's name.
        description (str): A brief description of the book.
        published_date (str): The publication date of the book (YYYY-MM-DD format).
        db (Session): The database session.

    Returns:
        RedirectResponse: Redirects to the book list after creation.
    """
    try:
        published_date_obj = datetime.strptime(published_date, "%Y-%m-%d").date()
        new_book = Book(
            title=title,
            author=author,
            description=description,
            published_date=published_date_obj
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        logging.debug(f"Book added: {new_book.title}")
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        logging.error(f"Error adding book: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/book/{book_id}", response_class=HTMLResponse)
async def book_detail(request: Request, book_id: int, db: Session = Depends(get_db)):
    """
    Displays the details of a specific book.

    Args:
        request (Request): The HTTP request object.
        book_id (int): The ID of the book to display.
        db (Session): The database session.

    Returns:
        HTMLResponse: The rendered HTML response with the book details.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book_detail.html", {"request": request, "book": book})


@app.get("/book/{book_id}/edit", response_class=HTMLResponse)
async def book_edit_form(request: Request, book_id: int, db: Session = Depends(get_db)):
    """
    Displays the form to edit a book.

    Args:
        request (Request): The HTTP request object.
        book_id (int): The ID of the book to edit.
        db (Session): The database session.

    Returns:
        HTMLResponse: The rendered HTML response with the book form.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book_form.html", {"request": request, "book": book})


@app.post("/book/{book_id}/edit", response_class=HTMLResponse)
async def book_edit(
    request: Request,
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    published_date: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Handles editing an existing book.

    Args:
        request (Request): The HTTP request object.
        book_id (int): The ID of the book to edit.
        title (str): The updated title of the book.
        author (str): The updated author's name.
        description (str): The updated description of the book.
        published_date (str): The updated publication date (YYYY-MM-DD format).
        db (Session): The database session.

    Returns:
        RedirectResponse: Redirects to the book detail view after editing.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book.title = title
    book.author = author
    book.description = description
    book.published_date = datetime.strptime(published_date, "%Y-%m-%d").date()
    db.commit()
    db.refresh(book)
    return RedirectResponse(url=f"/book/{book_id}", status_code=303)


@app.get("/book/{book_id}/delete", response_class=HTMLResponse)
async def book_delete_form(request: Request, book_id: int, db: Session = Depends(get_db)):
    """
    Displays the confirmation page to delete a book.

    Args:
        request (Request): The HTTP request object.
        book_id (int): The ID of the book to delete.
        db (Session): The database session.

    Returns:
        HTMLResponse: The rendered HTML response with the confirmation page.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book_confirm_delete.html", {"request": request, "book": book})


@app.post("/book/{book_id}/delete", response_class=HTMLResponse)
async def book_delete(book_id: int, db: Session = Depends(get_db)):
    """
    Handles deleting an existing book.

    Args:
        book_id (int): The ID of the book to delete.
        db (Session): The database session.

    Returns:
        RedirectResponse: Redirects to the book list after deletion.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
