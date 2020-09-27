# MD Notes

MD Notes is an online notes application. I created this application
for my own use, since I wasn't able to find any apps that fulfilled
my needs. MD Notes is a fully-online editor which allows creating
markdown flavored notes that support syntax highlighting as well as
the ability to render math in the LATEX format.

## Getting Started

The backend of this application consists of an SQLite database
managed by a Flask server hosted by Heroku. The backend server
consists of a RESTful API called by the React frontend hosted by
Netlify.  

### Dependencies

The dependencies of the backend are managed with `pipenv` (for the
Flask backend) and `npm` (for the React frontend).

Install `pipenv`:
```
$ pip install pipenv
```

Installing dependencies:
```
$ pipenv install
```
```
$ npm install
```

### Running the application

Get the Flask server to listen for requests on port 5000 by running:

```
$ flask run
``` 

And run a development version of the website with:
```
$ npm start
```

Then open your browser to [localhost:3000](http://localhost:3000).

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - web application framework
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) - creating RESTful API with flask
* [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for Python applications
* [React](https://reactjs.org/) - the UI for the web application
