from fastapi import HTTPException, status

InvalidCredentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Incorrect email or password',
    headers={'WWW-Authenticate': 'Basic'},
)

MovieAlreadyRegistered = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Movie already registered',
)

MovieNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Movie not found',
)

ReviewAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='You have already reviewed this movie',
)

LoginAlreadyRegistered = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Login already registered',
)

UserNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='User not found',
)

WrongYear = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='You entered the wrong year',
)
