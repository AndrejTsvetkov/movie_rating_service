from base64 import b64encode
from http import HTTPStatus

import pytest
from sqlalchemy.exc import IntegrityError

from app.exceptions import (
    InvalidCredentials,
    LoginAlreadyRegistered,
    MovieAlreadyRegistered,
    MovieNotFound,
    ReviewAlreadyExists,
    UserNotFound,
    WrongYear,
)


def headers_for_auth(login: str, password: str) -> dict[str, str]:
    headers = {}
    headers['Authorization'] = (
        'Basic ' + b64encode(f'{login}:{password}'.encode()).decode()
    )
    return headers


@pytest.mark.usefixtures('auth_mock')
def test_get_authorized_user(client):
    response = client.get(
        '/users/me', headers=headers_for_auth('test_user', '12345678')
    )
    assert response.status_code == HTTPStatus.OK, response.text
    data = response.json()
    assert data['login'] == 'test_user'
    assert data['id'] == 1


@pytest.mark.parametrize(
    ('login', 'password', 'is_mock_return_user'),
    [
        ('some_user', '12345678', False),
        ('test_user', 'password', False),
        ('some_user', 'some_pass', True),
    ],
    ids=[
        'incorrect_login',
        'incorrect_password',
        'incorrect_both',
    ],
)
def test_get_authorized_user_failed(  # pylint: disable=too-many-arguments
    client, get_user_by_login_mock, user, login, password, is_mock_return_user
):
    if is_mock_return_user:
        get_user_by_login_mock.return_value = user
    else:
        get_user_by_login_mock.return_value = None

    response = client.get('/users/me', headers=headers_for_auth(login, password))
    assert response.status_code == InvalidCredentials.status_code, response.text
    data = response.json()
    assert data['detail'] == InvalidCredentials.detail


@pytest.mark.usefixtures('auth_mock')
def test_get_user(client, get_user_mock, user):
    get_user_mock.return_value = user

    response = client.get('/users/1', headers=headers_for_auth('test_user', '12345678'))
    assert response.status_code == HTTPStatus.OK, response.text
    data = response.json()
    assert data['login'] == 'test_user'
    assert data['id'] == 1


@pytest.mark.usefixtures('auth_mock')
def test_get_user_failed(client, get_user_mock):
    get_user_mock.return_value = None

    response = client.get('/users/1', headers=headers_for_auth('test_user', '12345678'))
    assert response.status_code == UserNotFound.status_code, response.text
    data = response.json()
    assert data['detail'] == UserNotFound.detail


def test_create_user(client, get_user_by_login_mock, create_user_mock, user):
    get_user_by_login_mock.return_value = None
    create_user_mock.return_value = user

    response = client.post(
        '/users/',
        json={
            'login': 'test_user',
            'password': '12345678',
        },
    )

    assert response.status_code == HTTPStatus.OK, response.text
    data = response.json()
    assert data['login'] == 'test_user'
    assert data['id'] == 1


def test_create_user_failed(client, get_user_by_login_mock, user):
    get_user_by_login_mock.return_value = user

    response = client.post(
        '/users/',
        json={
            'login': 'test_user',
            'password': '12345678',
        },
    )

    assert response.status_code == LoginAlreadyRegistered.status_code, response.text
    data = response.json()
    assert data['detail'] == LoginAlreadyRegistered.detail


@pytest.mark.usefixtures('auth_mock')
def test_get_movie(client, movie, get_movie_mock):
    get_movie_mock.return_value = movie

    response = client.get(
        '/movies/1', headers=headers_for_auth('test_user', '12345678')
    )

    assert response.status_code == HTTPStatus.OK, response.text
    data = response.json()
    assert data['id'] == 1
    assert data['title'] == 'test_movie'
    assert data['release_year'] == 2010


@pytest.mark.usefixtures('auth_mock')
def test_get_movie_failed(client, get_movie_mock):
    get_movie_mock.return_value = None

    response = client.get(
        '/movies/1', headers=headers_for_auth('test_user', '12345678')
    )

    assert response.status_code == MovieNotFound.status_code, response.text
    data = response.json()
    assert data['detail'] == MovieNotFound.detail


@pytest.mark.usefixtures('auth_mock')
def test_create_movie(client, create_movie_mock, get_movie_by_title_mock, movie):
    get_movie_by_title_mock.return_value = None
    create_movie_mock.return_value = movie

    response = client.post(
        '/movies/',
        headers=headers_for_auth('test_user', '12345678'),
        json={
            'title': 'test_movie',
            'release_year': '2010',
        },
    )

    assert response.status_code == HTTPStatus.OK, response.text
    data = response.json()
    assert data['title'] == 'test_movie'
    assert data['release_year'] == 2010
    assert data['id'] == 1


@pytest.mark.usefixtures('auth_mock')
def test_create_already_registered_movie(client, get_movie_by_title_mock, movie):
    get_movie_by_title_mock.return_value = movie

    response = client.post(
        '/movies/',
        headers=headers_for_auth('test_user', '12345678'),
        json={
            'title': 'test_movie',
            'release_year': '2010',
        },
    )

    assert response.status_code == MovieAlreadyRegistered.status_code, response.text
    data = response.json()
    assert data['detail'] == MovieAlreadyRegistered.detail


@pytest.mark.usefixtures('auth_mock')
def test_create_movie_with_wrong_year(
    client, create_movie_mock, get_movie_by_title_mock
):
    get_movie_by_title_mock.return_value = None
    create_movie_mock.side_effect = IntegrityError('Mock', 'Mock', 'Mock')

    response = client.post(
        '/movies/',
        headers=headers_for_auth('test_user', '12345678'),
        json={
            'title': 'test_movie',
            'release_year': '2010',
        },
    )

    assert response.status_code == WrongYear.status_code, response.text
    data = response.json()
    assert data['detail'] == WrongYear.detail


@pytest.mark.usefixtures('auth_mock', 'update_movie_mock')
def test_add_review(client, get_movie_mock, movie, add_review_mock, review):
    get_movie_mock.return_value = movie
    add_review_mock.return_value = review

    response = client.post(
        '/reviews/',
        headers=headers_for_auth('test_user', '12345678'),
        json={
            'movie_id': 1,
            'score': 10,
            'review_text': 'Nice movie!',
        },
    )

    assert response.status_code == HTTPStatus.OK, response.text
    data = response.json()
    assert data['movie_id'] == 1
    assert data['score'] == 10
    assert data['review_text'] == 'Nice movie!'


@pytest.mark.usefixtures('auth_mock')
def test_add_review_of_unknown_movie(client, get_movie_mock):
    get_movie_mock.return_value = None

    response = client.post(
        '/reviews/',
        headers=headers_for_auth('test_user', '12345678'),
        json={
            'movie_id': 1,
            'score': 10,
            'review_text': 'Nice movie!',
        },
    )

    assert response.status_code == MovieNotFound.status_code, response.text
    data = response.json()
    assert data['detail'] == MovieNotFound.detail


@pytest.mark.usefixtures('auth_mock')
def test_add_already_existed_review(client, get_movie_mock, add_review_mock, movie):
    get_movie_mock.return_value = movie
    add_review_mock.side_effect = IntegrityError('Mock', 'Mock', 'Mock')

    response = client.post(
        '/reviews/',
        headers=headers_for_auth('test_user', '12345678'),
        json={
            'movie_id': 1,
            'score': 10,
            'review_text': 'Nice movie!',
        },
    )

    assert response.status_code == ReviewAlreadyExists.status_code, response.text
    data = response.json()
    assert data['detail'] == ReviewAlreadyExists.detail
