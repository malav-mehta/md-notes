# md-notes

## About

The complete Flask-based backend of a RESTful API for a markdown notes application. Implemented authentication on the API with JWT and used SQLAlchemy as the ORM. The server is deployed to Heroku.

## Running locally

First, clone the repo:

```shell
$ git clone https://github.com/malav-mehta/md-notes.git
$ cd md-notes
```

Then, install the `pipenv`:

```shell
$ pip install pipenv
```

Next, install all dependencies and get it running:

```shell
$ pipenv install
$ flask run
```

Finall, you can begin sending requests to [localhost:5000](http://localhost:5000).

## Tech stack

- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

If you find any bugs or have any questions, email me: [malavhmehta@outlook.com](mailto:malavhmehta@outlook.com).
