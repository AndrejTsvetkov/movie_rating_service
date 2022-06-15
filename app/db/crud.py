from typing import Optional

from sqlalchemy.orm import Query, Session

from app.db import models, schemas


# User stuff
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_login(db: Session, login: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.login == login).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(login=user.login)
    db_user.set_hashed_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Movie stuff
def get_movie(db: Session, movie_id: int) -> Optional[models.Movie]:
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def get_movie_by_title(db: Session, title: str) -> Optional[models.Movie]:
    return db.query(models.Movie).filter(models.Movie.title == title).first()


def create_movie(db: Session, movie: schemas.MovieCreate) -> models.Movie:
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie_statistic(db: Session, review: schemas.ReviewCreate) -> None:
    # get current movie in this review
    db_movie = get_movie(db, review.movie_id)
    if db_movie:
        db_movie.update_avg_score(new_score=review.score)
        db_movie.update_review_number(review_text=review.review_text)


def get_filtered_movies_query(
    db: Session, movie_filters: schemas.MovieFilters
) -> Query:
    filters = []
    if movie_filters.filter_by_text:
        filters.append(models.Movie.title.contains(movie_filters.filter_by_text))
    if movie_filters.filter_by_year:
        filters.append(models.Movie.release_year == movie_filters.filter_by_year)
    movie_query = db.query(models.Movie).filter(*filters)
    if movie_filters.sort_by_avg_score:
        movie_query = movie_query.order_by(models.Movie.avg_score.desc())

    return movie_query


# Review stuff
def add_review(
    db: Session, review: schemas.ReviewCreate, user_id: int
) -> models.Review:
    db_review = models.Review(**review.dict(), user_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
