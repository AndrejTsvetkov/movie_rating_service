from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    login = sa.Column(sa.String, unique=True, nullable=False)
    hashed_password = sa.Column(sa.String)

    reviews = relationship('Review', back_populates='user', uselist=True)

    def __repr__(self) -> str:
        return f'<User "{self.login}">'

    def set_hashed_password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)


class Movie(Base):
    __tablename__ = 'movies'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String, nullable=False)
    release_year = sa.Column(sa.Integer, nullable=False)

    # review statistic
    avg_score = sa.Column(sa.Float, default=0.0, nullable=False)
    score_number = sa.Column(sa.Integer, default=0, nullable=False)
    review_number = sa.Column(sa.Integer, default=0, nullable=False)

    reviews = relationship('Review', back_populates='movie', uselist=True)

    __table_args__ = (
        # The first widely known movie «L'Arrivée d'un train en gare de la Ciotat»
        # was released at 1895
        sa.CheckConstraint('release_year >= 1895'),
    )

    def __repr__(self) -> str:
        return f'<Movie "{self.title}">'

    def update_avg_score(self, new_score: int) -> None:
        old_score_sum = self.avg_score * self.score_number
        self.score_number += 1
        self.avg_score = (old_score_sum + new_score) / self.score_number

    def update_review_number(self, review_text: Optional[str]) -> None:
        if review_text is not None:
            self.review_number += 1


class Review(Base):
    __tablename__ = 'reviews'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    movie_id = sa.Column(sa.Integer, sa.ForeignKey(Movie.id))

    score = sa.Column(sa.SmallInteger, nullable=False)
    review_text = sa.Column(sa.Text, nullable=True)

    user = relationship('User', back_populates='reviews', uselist=False)
    movie = relationship('Movie', back_populates='reviews', uselist=False)

    def __repr__(self) -> str:
        return f'<Review of {self.movie} by {self.user} score = {self.score}>'

    __table_args__ = (
        sa.CheckConstraint('0 <= score AND score <= 10'),
        sa.UniqueConstraint('user_id', 'movie_id'),
    )
