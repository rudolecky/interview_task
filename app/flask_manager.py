import os
from flask import Flask, render_template
from flask.cli import FlaskGroup

from scraper import scrape_into_db
# import app


class Config(object):
    FLASK_ENV = 'development'
    FLASK_DEBUG = 1

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgres://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False



def render_flats():
    flats = scrape_into_db()

    return render_template("index.html", flats=flats)

def add_views(app):
    app.add_url_rule('/', view_func=render_flats)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    add_views(app)
    return app

app = create_app()

# def create_app(script_info=None):
#     app = Flask(__name__)
#     return app

# cli = FlaskGroup(app)


# if __name__ == "__main__":
#     cli()



# @app.route('/')
# def index():
#     data = scrape_into_db()
#     return render_template('index.html', flats=data)