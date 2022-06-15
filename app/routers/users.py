from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import crud, models, schemas
from app.db.schemas import HTTPError
from app.dependencies import auth_required, get_db
from app.exceptions import LoginAlreadyRegistered, UserNotFound

router = APIRouter(
    prefix='/users',
)


@router.post(
    '/',
    response_model=schemas.User,
    responses={
        LoginAlreadyRegistered.status_code: {
            'model': HTTPError,
            'description': LoginAlreadyRegistered.detail,
        }
    },
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> models.User:
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        raise LoginAlreadyRegistered
    return crud.create_user(db=db, user=user)


@router.get('/me', response_model=schemas.User)
def get_authorized_user(
    current_user: models.User = Depends(auth_required),
) -> models.User:
    return current_user


@router.get(
    '/{user_id}',
    response_model=schemas.User,
    responses={
        UserNotFound.status_code: {
            'model': HTTPError,
            'description': UserNotFound.detail,
        }
    },
    dependencies=[Depends(auth_required)],
)
def get_user(user_id: int, db: Session = Depends(get_db)) -> models.User:
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise UserNotFound
    return db_user
