# uvicorn main:app --reload


from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Request
from datetime import datetime
import logging

# Database Setup
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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/", response_class=HTMLResponse)
async def book_list(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return templates.TemplateResponse("book_list.html", {"request": request, "books": books})

@app.get("/book/new", response_class=HTMLResponse)
async def book_create_form(request: Request):
    return templates.TemplateResponse("book_form.html", {"request": request, "book": None})


@app.post("/book/new", response_class=HTMLResponse)
async def book_create(request: Request, title: str = Form(...), author: str = Form(...), 
                      description: str = Form(...), published_date: str = Form(...), db: Session = Depends(get_db)):
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
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book_detail.html", {"request": request, "book": book})

@app.get("/book/{book_id}/edit", response_class=HTMLResponse)
async def book_edit_form(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book_form.html", {"request": request, "book": book})

@app.post("/book/{book_id}/edit", response_class=HTMLResponse)
async def book_edit(request: Request, book_id: int, title: str = Form(...), author: str = Form(...), 
                    description: str = Form(...), published_date: str = Form(...), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book.title = title
    book.author = author
    book.description = description
    book.published_date = published_date
    db.commit()
    db.refresh(book)
    return RedirectResponse(url=f"/book/{book_id}", status_code=303)

@app.get("/book/{book_id}/delete", response_class=HTMLResponse)
async def book_delete_form(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book_confirm_delete.html", {"request": request, "book": book})

@app.post("/book/{book_id}/delete", response_class=HTMLResponse)
async def book_delete(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
