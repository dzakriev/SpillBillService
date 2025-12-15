import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from PIL import Image
import os

# Импорт вашего FastAPI приложения
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def valid_jpg_image():
    img = Image.new('RGB', (100, 100), color='white')
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer

@pytest.fixture
def invalid_txt_file():
    buffer = BytesIO(b"This is a text file content, not an image.")
    buffer.seek(0)
    return buffer

class TestBillParsingWithValidFiles:
    """Тесты эндпоинта get_bill_parsing с корректными файлами."""

    def test_upload_valid_jpg_returns_200(self, client, valid_jpg_image):
        """Проверка успешной загрузки JPG файла."""
        response = client.post(
            "/api/get_bill_parsing",
            files={"file": ("receipt.jpg", valid_jpg_image, "image/jpeg")}
        )
        
        assert response.status_code == 200

    def test_upload_valid_jpg_returns_json(self, client, valid_jpg_image):
        """Проверка, что ответ содержит корректный JSON."""
        response = client.post(
            "/api/get_bill_parsing",
            files={"file": ("receipt.jpg", valid_jpg_image, "image/jpeg")}
        )
        
        data = response.json()
        assert isinstance(data, dict)

    def test_upload_valid_jpg_contains_items(self, client, valid_jpg_image):
        response = client.post(
            "/api/get_bill_parsing",
            files={"file": ("receipt.jpg", valid_jpg_image, "image/jpeg")}
        )
        
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_response_item_structure(self, client, valid_jpg_image):
        response = client.post(
            "/api/get_bill_parsing",
            files={"file": ("receipt.jpg", valid_jpg_image, "image/jpeg")}
        )
        
        data = response.json()

        expected_fields = {"items", "total", "currency"}
        assert expected_fields.issubset(data.keys()) or "items" in data

class TestBillParsingWithInvalidFiles:

    def test_upload_txt_returns_400(self, client, invalid_txt_file):
        response = client.post(
            "/api/get_bill_parsing",
            files={"file": ("document.txt", invalid_txt_file, "text/plain")}
        )
        
        assert response.status_code == 400

    def test_upload_txt_returns_error_message(self, client, invalid_txt_file):
        response = client.post(
            "/api/get_bill_parsing",
            files={"file": ("document.txt", invalid_txt_file, "text/plain")}
        )
        
        data = response.json()
        assert "detail" in data or "error" in data

    def test_upload_txt_error_message_content(self, client, invalid_txt_file):
        response = client.post(
            "/api/get_bill_parsing",
            files={"file": ("document.txt", invalid_txt_file, "text/plain")}
        )
        
        data = response.json()
        error_message = data.get("detail", data.get("error", "")).lower()
        
        # Проверяем, что сообщение указывает на проблему с форматом файла
        assert any(word in error_message for word in ["format", "type", "image", "jpg", "png", "формат", "изображение"])

    def test_upload_no_file_returns_422(self, client):
        response = client.post("/api/get_bill_parsing")
        
        assert response.status_code == 422

    def test_upload_empty_file_returns_400(self, client):
        empty_buffer = BytesIO(b"")
        
        response = client.post(
            "/api/get_bill_parsing",
            files={"file": ("empty.jpg", empty_buffer, "image/jpeg")}
        )
        
        assert response.status_code in [400, 422]

    def test_upload_corrupted_image_returns_400(self, client):
        corrupted_buffer = BytesIO(b"not a real image content")
        
        response = client.post(
            "/api/get_bill_parsing",
            files={"file": ("corrupted.jpg", corrupted_buffer, "image/jpeg")}
        )
        
        assert response.status_code == 400

class TestHealthEndpoint:

    def test_health_returns_200(self, client):
        response = client.get("/api/health")
        
        assert response.status_code == 200

    def test_health_returns_json(self, client):
        response = client.get("/api/health")
        
        assert response.headers["content-type"] == "application/json"

    def test_health_returns_ok_status(self, client):
        response = client.get("/api/health")
        data = response.json()
        
        assert data.get("status") == "ok" or data.get("status") == "healthy"

    def test_health_response_structure(self, client):
        response = client.get("/api/health")
        data = response.json()
        
        assert "status" in data

    def test_health_no_auth_required(self, client):
        response = client.get("/api/health")

        assert response.status_code not in [401, 403]