from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import aio_pika
import json
import asyncio
import os

# Constants
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

# Initialize Database
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI App
app = FastAPI(
    title="Admin API",
    description="API for administrative tasks",
    version="1.0.0",
    contact={
        "name": "Admin API",
        "email": "balogunolalere@gmail.com",
    },
)

# Dependency
def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# RabbitMQ Connection
async def get_rabbitmq_connection():
    """Get a RabbitMQ connection."""
    return await aio_pika.connect_robust(RABBITMQ_URL)

# Publish Message to RabbitMQ
async def publish_message(connection, routing_key, data):
    """Publish a message to RabbitMQ."""
    channel = await connection.channel()
    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(data).encode()),
        routing_key=routing_key
    )

# API Endpoints
@app.post("/books/", response_model=schemas.Book, tags=["Books"])
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Create a new book."""
    db_book = crud.create_book(db=db, book=book)
    
    # Publish message to RabbitMQ
    connection = await get_rabbitmq_connection()
    await publish_message(connection, "book_updates", {"action": "create_book", "data": book.dict()})
    
    return db_book

@app.delete("/books/{book_id}", response_model=schemas.Book, tags=["Books"])
def remove_book(book_id: int, db: Session = Depends(get_db)):
    """Remove a book."""
    db_book = crud.remove_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/users/", response_model=list[schemas.User], tags=["Users"])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all users."""
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/borrowed-books/", response_model=list[schemas.UserWithBooks], tags=["Users", "Books"])
def list_users_with_borrowed_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all users with borrowed books."""
    return crud.get_users_with_borrowed_books(db, skip=skip, limit=limit)

@app.get("/books/unavailable/", response_model=list[schemas.Book], tags=["Books"])
def list_unavailable_books(db: Session = Depends(get_db)):
    """List all unavailable books."""
    return crud.get_unavailable_books(db)

# Consume Messages from RabbitMQ
async def consume_messages():
    """Consume messages from RabbitMQ."""
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue("user_book_updates")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body.decode())
                db = SessionLocal()
                if data["action"] == "create_user":
                    crud.create_user(db, schemas.UserCreate(**data["data"]))
                elif data["action"] == "borrow_book":
                    crud.create_borrowed_book(db, schemas.BorrowedBookCreate(**data["data"]))
                db.close()

# Startup Event
@app.on_event("startup")
async def startup_event():
    """Start consuming messages from RabbitMQ."""
    asyncio.create_task(consume_messages())