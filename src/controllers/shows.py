from flask import Blueprint, flash, render_template

from src.forms import ShowForm
from src.models.shows import Shows

shows_api = Blueprint("shows_api", __name__)


# READ ----------------------------------------------------
# List
@shows_api.route("/")
def shows():
    shows = Shows.query.order_by("start_time").all()
    return render_template("pages/shows.html", shows=shows)


#  CREATE -------------------------------------------------
# Form GET
@shows_api.route("/create")
def create_shows():
    return render_template("forms/new_show.html", form=ShowForm())


# Form SUBMIT
@shows_api.route("/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash("Show was successfully listed!")
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template("pages/home.html")
