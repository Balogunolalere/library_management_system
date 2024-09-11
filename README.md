# Library Management System

## Overview

This Library Management System is a microservices-based application designed to manage books and user interactions in a library setting. It consists of two main components:

1. Frontend API: Handles user-facing operations such as browsing books, user registration, and borrowing books.
2. Backend API: Manages administrative tasks like adding new books, removing books, and viewing user information.

The system uses PostgreSQL for data storage and RabbitMQ for message queuing between services.

## Tech Stack

- Python 3.9
- FastAPI
- PostgreSQL
- RabbitMQ
- Docker & Docker Compose

## Project Structure

```
library_management_system/
├── docker-compose.yml
├── frontend_api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── crud.py
│   │   ├── schemas.py
│   │   └── database.py
│   └── tests/
│       └── test_frontend_api.py
└── backend_api/
    ├── Dockerfile
    ├── requirements.txt
    ├── app/
    │   ├── main.py
    │   ├── models.py
    │   ├── crud.py
    │   ├── schemas.py
    │   └── database.py
    └── tests/
        └── test_backend_api.py
```

## Setup and Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/Balogunolalere/library_management_system.git
   cd library_management_system
   ```

2. Build and start the services:
   ```
   docker compose up --build
   ```

3. The services will be available at:
   - Frontend API: http://localhost:8000
   - Backend API: http://localhost:8001
   - RabbitMQ Management: http://localhost:15672 (guest/guest)

## API Documentation

Once the services are running, you can access the interactive API documentation:

- Frontend API: http://localhost:8000/docs
- Backend API: http://localhost:8001/docs

## Usage

### Frontend API

- Create a user: POST /users/
- List books: GET /books/
- Get a specific book: GET /books/{book_id}
- Filter books: GET /books/filter/
- Borrow a book: POST /books/{book_id}/borrow

### Backend API

- Create a book: POST /books/
- Remove a book: DELETE /books/{book_id}
- List users: GET /users/
- List users with borrowed books: GET /users/borrowed-books/
- List unavailable books: GET /books/unavailable/

## Testing

To run the tests, use the following commands:

For Frontend API:
```
pytest frontend_api/tests/
```

For Backend API:
```
pytest backend_api/tests/
```
