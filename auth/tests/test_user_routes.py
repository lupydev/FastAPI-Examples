import pytest
from unittest.mock import MagicMock, patch
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session
from uuid import uuid4

from auth.app.main import app
from auth.app.models.user import User
from auth.app.schemas.user import UserResponse
from auth.app.api.routes.user import get_db
from auth.app.core.config import settings

# Cliente de prueba
client = TestClient(app)


# Mock para la base de datos
@pytest.fixture
def mock_db():
    """Fixture que proporciona un mock de la base de datos"""
    mock = MagicMock(spec=Session)
    return mock


# Sobrescribir la dependencia de get_db
@pytest.fixture
def override_get_db(mock_db):
    """Fixture para sobrescribir la dependencia get_db con el mock"""
    app.dependency_overrides[get_db] = lambda: mock_db
    yield
    app.dependency_overrides = {}


# Tests para el endpoint de creación de usuario
class TestCreateUser:
    def test_create_user_success(self, mock_db, override_get_db):
        """Test para la creación exitosa de un usuario"""
        # Usuario de prueba a crear
        user_data = {
            "name": "test",
            "surname": "test",
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        }

        # Mock para las verificaciones de email y username (ambos no existen)
        email_mock = MagicMock()
        email_mock.first.return_value = None

        username_mock = MagicMock()
        username_mock.first.return_value = None

        # Configurar los resultados de las consultas
        mock_db.exec.side_effect = [email_mock, username_mock]

        # ID simulado para el nuevo usuario
        user_id = uuid4()

        # Datos del usuario que serán devueltos
        user_response_data = {
            "id": str(user_id),
            "username": user_data["username"],
            "name": user_data["name"],
            "surname": user_data["surname"],
            "email": user_data["email"],
        }

        # Guardar referencia al método original
        original_init = UserResponse.__init__

        # Definir la función de reemplazo
        def mock_init(self, **kwargs):
            # Convertir "results" a "user" como espera el esquema
            if "results" in kwargs:
                kwargs["user"] = kwargs.pop("results")
            original_init(self, **kwargs)

        # Aplicar los patches necesarios
        with patch.object(User, "model_dump", return_value=user_response_data):
            with patch.object(UserResponse, "__init__", mock_init):
                # Ejecutar la solicitud
                response = client.post(f"{settings.API}/user/", json=user_data)

        # Verificaciones
        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.json()
        assert response.json()["user"]["username"] == user_data["username"]
        assert response.json()["user"]["email"] == user_data["email"]

        # Verificar que los métodos de DB fueron llamados
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    def test_create_user_email_exists(self, mock_db, override_get_db):
        """Test para verificar el error cuando el email ya existe"""
        # Configurar mock para que encuentre un usuario con el mismo email
        mock_exec = MagicMock()
        mock_exec.first.return_value = User(
            id=uuid4(), username="existinguser", email="test@example.com"
        )
        mock_db.exec.return_value = mock_exec

        # Usuario de prueba con email existente
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        }

        response = client.post(f"{settings.API}/user/", json=user_data)

        # Verificaciones
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "El correo electrónico ya existe" in response.json()["detail"]

    def test_create_user_username_exists(self, mock_db, override_get_db):
        """Test para verificar el error cuando el username ya existe"""
        # Primera consulta (email) devuelve None
        mock_exec1 = MagicMock()
        mock_exec1.first.return_value = None

        # Segunda consulta (username) devuelve un usuario existente
        mock_exec2 = MagicMock()
        mock_exec2.first.return_value = User(
            id=uuid4(), username="testuser", email="other@example.com"
        )

        # Configurar que la primera llamada devuelva mock_exec1 y la segunda mock_exec2
        mock_db.exec.side_effect = [mock_exec1, mock_exec2]

        # Usuario de prueba con username existente
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        }

        response = client.post(f"{settings.API}/user/", json=user_data)

        # Verificaciones
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "El nombre de usuario ya existe" in response.json()["detail"]

    def test_create_user_db_error(self, mock_db, override_get_db):
        """Test para verificar el manejo de errores de base de datos"""
        # Configurar mock para que no encuentre usuarios existentes
        mock_exec = MagicMock()
        mock_exec.first.return_value = None
        mock_db.exec.return_value = mock_exec

        # Usuario de prueba a crear
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        }

        # Simular error en commit
        mock_db.add.return_value = None
        mock_db.commit.side_effect = Exception("Error de base de datos")

        # IMPORTANTE: No hacer patch de la clase User completa
        # En su lugar, podemos hacer patch de model_dump() si es necesario
        with patch.object(User, "model_dump", return_value={}):
            response = client.post(f"{settings.API}/user/", json=user_data)

        # Verificaciones
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error al crear el usuario" in response.json()["detail"]

        # Verificar que se llamó a rollback
        mock_db.rollback.assert_called_once()
