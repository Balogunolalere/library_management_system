from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import aio_pika
import asyncio
import json
import os

# Create all tables in the engine
models.Base.metadata.create_all(bind=engine)

# RabbitMQ URL
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

# Initialize FastAPI app
app = FastAPI(
    title="Frontend API",
    description="API for users",
    version="1.0.0",
)
# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to publish message to RabbitMQ
async def publish_message(routing_key, message_data):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message_data).encode()),
            routing_key=routing_key
        )

# Create user endpoint
@app.post("/users/", response_model=schemas.User, tags=["Users"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    await publish_message("user_book_updates", {"action": "create_user", "data": user.dict()})
    return db_user

# List books endpoint
@app.get("/books/", response_model=list[schemas.Book], tags=["Books"])
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)

# Get book endpoint
@app.get("/books/{book_id}", response_model=schemas.Book, tags=["Books"])
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Filter books endpoint
@app.get("/books/filter/", tags=["Books"])
def filter_books(publisher: str = None, category: str = None, db: Session = Depends(get_db)):
    return crud.filter_books(db, publisher=publisher, category=category)

# Borrow book endpoint
@app.post("/books/{book_id}/borrow", tags=["Books", "Users"])
async def borrow_book(book_id: int, user_id: int, days: int, db: Session = Depends(get_db)):
    borrowed_book = crud.borrow_book(db, book_id=book_id, user_id=user_id, days=days)
    if borrowed_book is None:
        raise HTTPException(status_code=404, detail="Book not found or not available")
    await publish_message("user_book_updates", {
        "action": "borrow_book",
        "data": {
            "user_id": user_id,
            "book_id": book_id,
            "borrow_date": borrowed_book.borrow_date.isoformat(),
            "return_date": borrowed_book.return_date.isoformat()
        }
    })
    return borrowed_book

# Consume messages from RabbitMQ
async def consume_messages():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("book_updates")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                message_data = json.loads(message.body.decode())
                if message_data["action"] == "create_book":
                    book_data = message_data["data"]
                    book_create = schemas.BookCreate(**book_data)
                    db = SessionLocal()
                    try:
                        crud.create_book(db, book_create)
                    finally:
                        db.close()

# Start consuming messages on startup
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_messages())