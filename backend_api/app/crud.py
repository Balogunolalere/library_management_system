from sqlalchemy.orm import Session
from . import models, schemas

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict(), available=True)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def remove_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_users_with_borrowed_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).join(models.BorrowedBook).offset(skip).limit(limit).all()

def get_unavailable_books(db: Session):
    return db.query(models.Book).filter(models.Book.available == False).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_borrowed_book(db: Session, borrowed_book: schemas.BorrowedBookCreate):
    db_borrowed_book = models.BorrowedBook(**borrowed_book.dict())
    db.add(db_borrowed_book)
    db_book = db.query(models.Book).filter(models.Book.id == borrowed_book.book_id).first()
    if db_book:
        db_book.available = False
    db.commit()
    db.refresh(db_borrowed_book)
    return db_borrowed_book