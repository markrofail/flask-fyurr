import logging
from logging import FileHandler, Formatter

import babel
import dateutil.parser
from flask import Flask
from flask.templating import render_template
from flask_migrate import Migrate
from flask_moment import Moment

from src.controllers import artist_api, shows_api, venues_api
from src.models import db

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#


def create_app():
    app = Flask(__name__)

    # apply configuration
    app.config.from_object("config")

    # initialize extensions
    migrate = Migrate()
    moment = Moment()

    # register extensions
    moment.init_app(app)
    migrate.init_app(app, db)
    db.init_app(app)

    if not app.debug:
        file_handler = FileHandler("error.log")
        file_handler.setFormatter(
            Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info("errors")

    return app


app = create_app()

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


app.register_blueprint(venues_api, url_prefix="/venues")
app.register_blueprint(shows_api, url_prefix="/shows")
app.register_blueprint(artist_api, url_prefix="/artists")

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

if __name__ == "__main__":
    app.run()
