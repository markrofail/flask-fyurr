import logging

from flask_fixtures import load_fixtures_from_file
from flask_migrate import MigrateCommand
from flask_script import Manager
from sqlalchemy.exc import IntegrityError

from fyuur import create_app, db

logger = logging.getLogger(__name__)

manager = Manager(create_app)


def loan_fixtures(fixtures):
    for fixture in fixtures:
        try:
            load_fixtures_from_file(
                db=db, fixture_filename=f"fyuur/fixtures/{fixture}.json"
            )
        except IntegrityError:
            pass


@manager.option(dest="fixture")
def load_db(fixture):
    if fixture == "all":
        loan_fixtures(["location", "genres", "artists", "venues", "shows"])
    else:
        loan_fixtures([fixture])


@manager.command
def run():
    manager.app.run(host="0.0.0.0", port=8080)


manager.add_command("db", MigrateCommand)
manager.run()
