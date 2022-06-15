from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import crud, models, schemas
from app.db.schemas import HTTPError
from app.dependencies import auth_required, get_db
from app.exceptions import MovieNotFound, ReviewAlreadyExists

router = APIRouter(
    prefix='/reviews',
    responses={
        MovieNotFound.status_code: {
            'model': HTTPError,
            'description': MovieNotFound.detail,
        },
        ReviewAlreadyExists.status_code: {
            'model': HTTPError,
            'description': ReviewAlreadyExists.detail,
        },
    },
)


@router.post('/', response_model=schemas.Review)
def add_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_required),
) -> models.Review:

    if not crud.get_movie(db, movie_id=review.movie_id):
        raise MovieNotFound

    try:
        db_review = crud.add_review(db, review=review, user_id=current_user.id)
        # in update function we won't get any error because we already add review correctly
        crud.update_movie_statistic(db, review=review)
        return db_review
    except IntegrityError as err:
        raise ReviewAlreadyExists from err
