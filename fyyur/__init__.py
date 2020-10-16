import logging
from logging import FileHandler, Formatter

import babel
import dateutil.parser
from flask import Flask
from flask.templating import render_template
from flask_migrate import Migrate
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect

from fyyur.controllers import artists_views, shows_views, venues_views
from fyyur.models import db

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#


def create_app(config_path="settings:local"):
    app = Flask(__name__)

    # apply configuration
    app.config.from_object(config_path)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

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


def register_extensions(app):
    """Register Flask extensions."""
    # initialize extensions
    migrate = Migrate()
    moment = Moment()
    csrf = CSRFProtect()

    # register extensions
    moment.init_app(app)
    migrate.init_app(app, db)
    db.init_app(app)

    csrf.init_app(app)
    csrf.exempt("fyyur.controllers.venues.search_venues")
    csrf.exempt("fyyur.controllers.venues.delete_venue")
    csrf.exempt("fyyur.controllers.artists.search_artists")

    app.jinja_env.filters["datetime"] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers
# ----------------------------------------------------------------------------#


def register_blueprints(app):
    """Register Flask blueprints."""

    def index():
        return render_template("pages/home.html")

    app.add_url_rule("/", "index", view_func=index)
    app.register_blueprint(venues_views, url_prefix="/venues")
    app.register_blueprint(shows_views, url_prefix="/shows")
    app.register_blueprint(artists_views, url_prefix="/artists")


def register_errorhandlers(app):
    """Register error handlers."""

    def not_found_error(error):
        return render_template("errors/404.html"), 404

    def server_error(error):
        return render_template("errors/500.html"), 500

    app.errorhandler(404)(not_found_error)
    app.errorhandler(500)(server_error)


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
