from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).filter(models.Book.available == True).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def filter_books(db: Session, publisher: str = None, category: str = None):
    query = db.query(models.Book).filter(models.Book.available == True)
    if publisher:
        query = query.filter(models.Book.publisher == publisher)
    if category:
        query = query.filter(models.Book.category == category)
    return query.all()

def borrow_book(db: Session, book_id: int, user_id: int, days: int):
    book = db.query(models.Book).filter(models.Book.id == book_id, models.Book.available == True).first()
    if not book:
        return None
    
    book.available = False
    borrowed_book = models.BorrowedBook(
        user_id=user_id,
        book_id=book_id,
        borrow_date=datetime.utcnow(),
        return_date=datetime.utcnow() + timedelta(days=days)
    )
    db.add(borrowed_book)
    db.commit()
    db.refresh(borrowed_book)
    return borrowed_book

def add_book_from_message(db: Session, book_data: dict):
    db_book = models.Book(**book_data)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict(), available=True)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book