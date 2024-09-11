from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email: str
    firstname: str
    lastname: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author: str
    publisher: str
    category: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    available: bool

    class Config:
        orm_mode = True

class BorrowedBookBase(BaseModel):
    book_id: int
    borrow_date: datetime
    return_date: datetime

class BorrowedBookCreate(BorrowedBookBase):
    user_id: int

class BorrowedBook(BorrowedBookBase):
    id: int
    user: User
    book: Book

    class Config:
        orm_mode = True