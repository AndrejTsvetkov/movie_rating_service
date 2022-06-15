from typing import Generator

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.db import crud, models
from app.db.database import get_session
from app.exceptions import InvalidCredentials

security = HTTPBasic()


def get_db() -> Generator[Session, None, None]:
    session_local = get_session()
    db = session_local()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def auth_required(
    credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
) -> models.User:
    db_user = crud.get_user_by_login(db, login=credentials.username)
    if not (db_user and db_user.check_password(credentials.password)):
        raise InvalidCredentials

    return db_user
