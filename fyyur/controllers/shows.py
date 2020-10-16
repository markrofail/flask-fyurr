import logging

from flask import Blueprint, flash, render_template, request
from sqlalchemy.exc import IntegrityError

from fyyur.forms import ShowForm
from fyyur.models import db
from fyyur.models.shows import Show
from fyyur.utils import flash_error, parse_errors

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
    form = ShowForm(request.form)
    error = False

    if not form.validate():
        errors = parse_errors(form.errors)
        flash_error(errors)
        return render_template("forms/new_show.html", form=form)

    try:
        show = Show(
            start_time=form.start_time.data,
            venue_id=form.venue_id.data,
            artist_id=form.artist_id.data,
        )
        db.session.add(show)
        db.session.commit()
    except IntegrityError as exec:
        logger.error(exec)
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        flash_error("An error occurred. Show could not be listed.")
        return render_template("forms/new_show.html", form=form)
    else:
        flash("Show was successfully listed!")
        return render_template("pages/home.html")
