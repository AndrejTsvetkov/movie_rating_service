import pytest

from app.db import crud, models, schemas


# User stuff
@pytest.mark.usefixtures('user')
def test_get_user(db_session):
    user = crud.get_user(db_session, user_id=1)
    assert user.login == 'test_user'  # type: ignore


@pytest.mark.usefixtures('user')
def test_get_unknown_user(db_session):
    user = crud.get_user(db_session, user_id=3)
    assert user is None


@pytest.mark.usefixtures('user')
def test_get_user_by_login(db_session):
    user = crud.get_user_by_login(db_session, login='test_user')
    assert user.login == 'test_user'  # type: ignore


@pytest.mark.usefixtures('user')
def test_get_unknown_user_by_login(db_session):
    user = crud.get_user_by_login(db_session, login='non_existing_user')
    assert user is None


def test_create_user(db_session):
    user_schema = schemas.UserCreate(login='test_user', password='password')
    crud.create_user(db_session, user_schema)

    created_user = (
        db_session.query(models.User).filter(models.User.login == 'test_user').first()
    )

    assert created_user is not None
    assert created_user.check_password('password')


# Movie stuff
@pytest.mark.usefixtures('movie')
def test_get_movie(db_session):
    movie = crud.get_movie(db_session, movie_id=1)
    assert movie.title == 'test_movie'  # type: ignore


@pytest.mark.usefixtures('movie')
def test_get_unknown_movie(db_session):
    movie = crud.get_movie(db_session, movie_id=5)
    assert movie is None


@pytest.mark.usefixtures('movie')
def test_get_movie_by_title(db_session):
    movie = crud.get_movie_by_title(db_session, title='test_movie')
    assert movie.title == 'test_movie'  # type: ignore


@pytest.mark.usefixtures('movie')
def test_get_unknown_movie_by_title(db_session):
    movie = crud.get_movie_by_title(db_session, title='non_existing_movie')
    assert movie is None


def test_create_movie(db_session):
    movie_schema = schemas.MovieCreate(title='test_movie', release_year=2008)
    crud.create_movie(db_session, movie_schema)

    created_movie = (
        db_session.query(models.Movie)
        .filter(models.Movie.title == 'test_movie')
        .first()
    )

    assert created_movie is not None


@pytest.mark.parametrize(
    ('movie_id', 'score', 'review_text', 'score_number', 'avg_score', 'review_number'),
    [
        (1, 10, None, 1, 10.0, 0),
        (1, 8, 'Nice movie!', 1, 8.0, 1),
        (2, 4, 'Do not like it!', 3, 5.0, 2),
        (3, 8, None, 8, 6.25, 7),
    ],
)
@pytest.mark.usefixtures('movies')
def test_update_movie_statistic(  # pylint: disable=too-many-arguments
    db_session, movie_id, score, review_text, score_number, avg_score, review_number
):
    review = schemas.ReviewCreate(
        movie_id=movie_id, score=score, review_text=review_text
    )
    crud.update_movie_statistic(db_session, review)

    created_movie = (
        db_session.query(models.Movie).filter(models.Movie.id == movie_id).first()
    )

    assert created_movie.score_number == score_number
    assert created_movie.avg_score == avg_score
    assert created_movie.review_number == review_number


@pytest.mark.parametrize(
    ('filter_by_text', 'filter_by_year', 'result'),
    [
        ('Te', None, 2),
        ('Harry Potter', None, 0),
        ('', 2015, 1),
    ],
    ids=[
        'two_movies_fit',
        'do_not_fit_any_movie',
        'one_movies_fit',
    ],
)
@pytest.mark.usefixtures('movies')
def test_get_movies_by_filters(db_session, filter_by_text, filter_by_year, result):
    movie_filters = schemas.MovieFilters(
        filter_by_text=filter_by_text, filter_by_year=filter_by_year
    )
    query = crud.get_filtered_movies_query(db_session, movie_filters)

    assert len(query.all()) == result


@pytest.mark.parametrize(
    ('sort_by_avg_score', 'first_movie_title'),
    [
        (True, 'Tenet'),
        (False, 'Inception'),
    ],
)
@pytest.mark.usefixtures('movies')
def test_get_movies_by_filters_avg(db_session, sort_by_avg_score, first_movie_title):
    movie_filters = schemas.MovieFilters(sort_by_avg_score=sort_by_avg_score)
    query = crud.get_filtered_movies_query(db_session, movie_filters)

    movie_list = query.all()
    assert movie_list[0].title == first_movie_title


# Review stuff
@pytest.mark.usefixtures('user', 'movie')
def test_add_review(db_session):
    review_schema = schemas.ReviewCreate(
        movie_id=1, score=3, review_text='Very big review'
    )
    crud.add_review(db_session, review_schema, user_id=1)

    created_review = (
        db_session.query(models.Review).filter(models.Review.id == 1).first()
    )
    assert created_review is not None
