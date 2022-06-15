from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class MovieBase(BaseModel):
    title: str
    release_year: int = Field(ge=1895, le=date.today().year)


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True


class ExtMovie(Movie):
    avg_score: float
    score_number: int
    review_number: int


class MovieFilters(BaseModel):
    filter_by_text: Optional[str] = ''
    filter_by_year: Optional[int]
    sort_by_avg_score: Optional[bool] = False


class ReviewBase(BaseModel):
    pass


class ReviewCreate(ReviewBase):
    movie_id: int
    score: int = Field(ge=0, le=10)
    review_text: Optional[str]


class Review(ReviewCreate):
    class Config:
        orm_mode = True


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            'example': {'detail': 'HTTP Exception'},
        }
