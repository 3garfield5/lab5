from fastapi.testclient import TestClient
from fastapi import status

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]


def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]


def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user_data = {
        'name': 'New User',
        'email': 'new.user@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.json(), int)  # Проверяем что вернулся ID

    # Проверяем что пользователь действительно создался
    check_response = client.get("/api/v1/user", params={'email': new_user_data['email']})
    assert check_response.status_code == 200
    assert check_response.json()['email'] == new_user_data['email']


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_email = users[0]['email']
    duplicate_user_data = {
        'name': 'Duplicate User',
        'email': existing_email
    }
    response = client.post("/api/v1/user", json=duplicate_user_data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'User with this email already exists'}


def test_delete_user():
    '''Удаление пользователя'''
    # Сначала создадим пользователя для удаления
    temp_user_data = {
        'name': 'Temp User',
        'email': 'temp.user@mail.com'
    }
    create_response = client.post("/api/v1/user", json=temp_user_data)
    user_id = create_response.json()

    # Удаляем пользователя
    delete_response = client.delete("/api/v1/user", params={'email': temp_user_data['email']})
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Проверяем что пользователь действительно удалён
    check_response = client.get("/api/v1/user", params={'email': temp_user_data['email']})
    assert check_response.status_code == status.HTTP_404_NOT_FOUND