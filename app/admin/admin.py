import warnings

from flask import Flask
from flask_admin import Admin

from app.admin.views import MovieView, ReviewView, UserView
from app.db import models
from app.db.database import get_session


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = 'very_secret_key'
    admin = Admin(app)

    session = get_session()()
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'Fields missing from ruleset', UserWarning)
        admin.add_view(UserView(models.User, session))
        admin.add_view(MovieView(models.Movie, session))
        admin.add_view(ReviewView(models.Review, session))

    return app


if __name__ == '__main__':  # pragma: no cover
    create_app().run()
