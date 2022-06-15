# pylint: disable=W0621
import os
import tempfile
from contextlib import contextmanager

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import models


def get_engine(db_file):
    return create_engine(
        f'sqlite:///{db_file}',
        connect_args={'check_same_thread': False},
    )


def get_session(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def create_session(engine):
    session = get_session(engine)()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@pytest.fixture()
def _init_db():
    db_fd, db_file = tempfile.mkstemp()

    engine = get_engine(db_file)
    models.Base.metadata.create_all(bind=engine)

    with create_session(engine) as local_session:
        yield local_session

    models.Base.metadata.drop_all(bind=engine)
    os.close(db_fd)
    os.unlink(db_file)


@pytest.fixture()
def db_session(_init_db):
    return _init_db


@pytest.fixture()
def user(db_session):
    user = models.User(login='test_user')
    user.set_hashed_password('password')
    db_session.add(user)
    db_session.commit()


@pytest.fixture()
def movie(db_session):
    movie = models.Movie(title='test_movie', release_year=2010)
    db_session.add(movie)
    db_session.commit()


@pytest.fixture()
def movies(db_session):
    first_movie = models.Movie(id=1, title='Inception', release_year=2010)
    second_movie = models.Movie(
        id=2,
        title='Terminator Genisys',
        release_year=2015,
        avg_score=5.5,
        score_number=2,
        review_number=1,
    )
    third_movie = models.Movie(
        id=3,
        title='Tenet',
        release_year=2020,
        avg_score=6.0,
        score_number=7,
        review_number=7,
    )

    db_session.add(first_movie)
    db_session.add(second_movie)
    db_session.add(third_movie)
    db_session.commit()
