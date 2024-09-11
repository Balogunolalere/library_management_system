import httpx

ADMIN_API_BASE_URL = "http://127.0.0.1:8001"
FRONTEND_API_BASE_URL = "http://127.0.0.1:8000"

def create_book_on_admin(client, book_data):
    response = client.post(f"{ADMIN_API_BASE_URL}/books/", json=book_data)
    assert response.status_code == 200
    return response.json()["id"]

def test_create_user():
    with httpx.Client() as client:
        response = client.post(
            f"{FRONTEND_API_BASE_URL}/users/",
            json={"email": "test@example.com", "firstname": "Test", "lastname": "User"}
        )
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

def test_list_books():
    with httpx.Client() as client:
        # First, create a book on the admin API
        book_data = {"title": "Test Book", "author": "Test Author", "publisher": "Test Publisher", "category": "Test Category"}
        create_book_on_admin(client, book_data)

        response = client.get(f"{FRONTEND_API_BASE_URL}/books/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_get_book():
    with httpx.Client() as client:
        # First, create a book on the admin API
        book_data = {"title": "Test Book", "author": "Test Author", "publisher": "Test Publisher", "category": "Test Category"}
        book_id = create_book_on_admin(client, book_data)

        response = client.get(f"{FRONTEND_API_BASE_URL}/books/{book_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Test Book"

def test_filter_books():
    with httpx.Client() as client:
        # First, create a book on the admin API
        book_data = {"title": "Test Book", "author": "Test Author", "publisher": "Test Publisher", "category": "Test Category"}
        create_book_on_admin(client, book_data)

        response = client.get(f"{FRONTEND_API_BASE_URL}/books/filter/?publisher=Test Publisher&category=Test Category")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_borrow_book():
    with httpx.Client() as client:
        # First, create a user on the frontend API
        user_data = {"email": "borrower@example.com", "firstname": "Borrower", "lastname": "Test"}
        create_user_response = client.post(f"{FRONTEND_API_BASE_URL}/users/", json=user_data)
        assert create_user_response.status_code == 200
        user_id = create_user_response.json()["id"]

        # Then, create a book on the admin API
        book_data = {"title": "Borrow Me", "author": "Test Author", "publisher": "Test Publisher", "category": "Test Category"}
        book_id = create_book_on_admin(client, book_data)

        # Now, borrow the book on the frontend API
        response = client.post(f"{FRONTEND_API_BASE_URL}/books/{book_id}/borrow?user_id={user_id}&days=7")
        assert response.status_code == 200
        assert response.json()["book_id"] == book_id
        assert response.json()["user_id"] == user_id
