import logging

from flask import Blueprint, abort, flash, render_template, request
from sqlalchemy.exc import IntegrityError

from src.forms import ShowForm
from src.models import db
from src.models.shows import Show

logger = logging.getLogger(__name__)
shows_views = Blueprint("shows", __name__)


# READ ----------------------------------------------------
# List
@shows_views.route("/")
def shows_list():
    shows = Show.query.order_by("start_time").all()
    return render_template("pages/shows.html", shows=shows)


#  CREATE -------------------------------------------------
# Form GET
@shows_views.route("/create")
def create_shows():
    return render_template("forms/new_show.html", form=ShowForm())


# Form SUBMIT
@shows_views.route("/create", methods=["POST"])
def create_show_submission():
    error = False
    try:
        show = Show(
            start_time=request.form.get("start_time"),
            venue_id=request.form.get("venue_id"),
            artist_id=request.form.get("artist_id"),
        )
        db.session.add(show)
        db.session.commit()
    except IntegrityError as e:
        logger.error(e)
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        flash("An error occurred. Show could not be listed.")
        abort(500)
    else:
        flash("Show was successfully listed!")
        return render_template("pages/home.html")
