import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers import movies, reviews, users

app = FastAPI()

app.include_router(reviews.router)
app.include_router(movies.router)
app.include_router(users.router)
add_pagination(app)


if __name__ == '__main__':  # pragma: no cover (for debug purposes)
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
