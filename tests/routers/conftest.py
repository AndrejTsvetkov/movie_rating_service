# pylint: disable=W0621
import pytest
from fastapi.testclient import TestClient

from app.db import models
from app.main import app


@pytest.fixture(scope='session')
def client():
    test_client = TestClient(app)
    return test_client


@pytest.fixture()
def get_user_by_login_mock(mocker):
    return mocker.patch('app.db.crud.get_user_by_login')


@pytest.fixture()
def get_user_mock(mocker):
    return mocker.patch('app.db.crud.get_user')


@pytest.fixture()
def create_user_mock(mocker):
    return mocker.patch('app.db.crud.create_user')


@pytest.fixture()
def user():
    user = models.User(id=1, login='test_user')
    user.set_hashed_password('12345678')
    return user


@pytest.fixture()
def movie():
    return models.Movie(
        id=1,
        title='test_movie',
        release_year=2010,
        avg_score=0.0,
        score_number=0,
        review_number=0,
    )


@pytest.fixture()
def get_movie_mock(mocker):
    return mocker.patch('app.db.crud.get_movie')


@pytest.fixture()
def get_movie_by_title_mock(mocker):
    return mocker.patch('app.db.crud.get_movie_by_title')


@pytest.fixture()
def create_movie_mock(mocker):
    return mocker.patch('app.db.crud.create_movie')


@pytest.fixture()
def add_review_mock(mocker):
    return mocker.patch('app.db.crud.add_review')


@pytest.fixture()
def update_movie_mock(mocker):
    mocker.patch('app.db.crud.update_movie_statistic')


@pytest.fixture()
def review():
    return models.Review(
        id=1, user_id=1, movie_id=1, score=10, review_text='Nice movie!'
    )


@pytest.fixture()
def auth_mock(get_user_by_login_mock, user):
    # here we mock get_user_by_login function that is used in auth dependency
    # now we can authorize with user's credentials ('test_user', '12345678')
    get_user_by_login_mock.return_value = user
