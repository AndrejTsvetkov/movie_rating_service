# Movie Rating Service

## Description:
A movie rating service where users can rate movies and give reviews, 
as well as see movie ratings.

## Makefile commands

### Create venv:
    make venv

### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format

### Init database
    make init_db

### Run service:
    make up

You can then access the service at 
```
http://localhost:80/
```

and admin panel at:
```
http://localhost:5000/admin
```



## API Endpoints

| HTTP Method | Endpoint           | Action                                                      | Auth required |
|-------------|--------------------|-------------------------------------------------------------|-------------|
| POST        | /users/            | To sign up a new user account                               | No |
| GET         | /users/{user_id}   | To get user information with the specified `user_id`        | Yes |
| GET         | /users/me          | To get information about your account                       | Yes |
| POST        | /movies/           | To create a new movie                                       | Yes |
| GET         | /movies/{movie_id} | To get information about movie whose id is `movie_id`       | Yes |
| GET         | /movies            | To get a list of movies with certain filters and pagination | Yes |
| POST        | /reviews/          | To add a movie review                                      | Yes |

Note that you have to be authorized to fully  use the service, so make sure you
create an account before doing anything.

To get full details about endpoints go to  
```
http://localhost:80/docs
```


## Technologies Used

- Python
- Poetry
- FastAPI
- Flask-Admin
- SQLAlchemy
- Pytest
- Git
- GitHub
- Docker
- Docker Compose

## Authors

- [@AndrejTsvetkov](https://www.github.com/AndrejTsvetkov)
