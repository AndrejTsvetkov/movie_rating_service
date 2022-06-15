from typing import Any

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import crud, models, schemas
from app.db.schemas import HTTPError
from app.dependencies import auth_required, get_db
from app.exceptions import MovieAlreadyRegistered, MovieNotFound, WrongYear

router = APIRouter(
    prefix='/movies',
    dependencies=[Depends(auth_required)],
)


@router.post(
    '/',
    response_model=schemas.Movie,
    responses={
        MovieAlreadyRegistered.status_code: {
            'model': HTTPError,
            'description': MovieAlreadyRegistered.detail,
        },
        WrongYear.status_code: {
            'model': HTTPError,
            'description': WrongYear.detail,
        },
    },
)
def create_movie(
    movie: schemas.MovieCreate, db: Session = Depends(get_db)
) -> models.Movie:
    db_movie = crud.get_movie_by_title(db, title=movie.title)
    # сами вызвали исключение -> (context manager) -> передается в генератор ->
    # генератор рерайзнул его и он передался в Exception Handler
    if db_movie:
        raise MovieAlreadyRegistered
    # здесь Integrity Error и Exception Handler не может её обработать
    # (если нет try except) -> Internal server Error
    try:
        return crud.create_movie(db=db, movie=movie)
    except IntegrityError as err:
        raise WrongYear from err


@router.get(  # pragma: no cover  Can't construct query object without db connection
    '/',
    response_model=Page[schemas.ExtMovie],
)
def get_movies(
    movie_filters: schemas.MovieFilters = Depends(), db: Session = Depends(get_db)
) -> AbstractPage[Any]:
    return paginate(crud.get_filtered_movies_query(db, movie_filters))


@router.get(
    '/{movie_id}',
    response_model=schemas.ExtMovie,
    responses={
        MovieNotFound.status_code: {
            'model': HTTPError,
            'description': MovieNotFound.detail,
        }
    },
)
def get_movie(movie_id: int, db: Session = Depends(get_db)) -> models.Movie:
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise MovieNotFound
    return db_movie
