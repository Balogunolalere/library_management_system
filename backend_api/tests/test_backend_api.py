import httpx

API_BASE_URL = "http://127.0.0.1:8001"

def test_create_book():
    with httpx.Client() as client:
        response = client.post(
            f"{API_BASE_URL}/books/",
            json={"title": "Test Book", "author": "Test Author", "publisher": "Test Publisher", "category": "Test Category"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Test Book"

def test_remove_book():
    with httpx.Client() as client:
        # First, create a book
        book_data = {"title": "Remove Me", "author": "Test Author", "publisher": "Test Publisher", "category": "Test Category"}
        create_response = client.post(f"{API_BASE_URL}/books/", json=book_data)
        assert create_response.status_code == 200
        book_id = create_response.json()["id"]

        # Now, remove the book
        remove_response = client.delete(f"{API_BASE_URL}/books/{book_id}")
        assert remove_response.status_code == 200
        assert remove_response.json()["title"] == "Remove Me"

def test_list_users():
    with httpx.Client() as client:
        response = client.get(f"{API_BASE_URL}/users/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_list_users_with_borrowed_books():
    with httpx.Client() as client:
        response = client.get(f"{API_BASE_URL}/users/borrowed-books/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_list_unavailable_books():
    with httpx.Client() as client:
        response = client.get(f"{API_BASE_URL}/books/unavailable/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
