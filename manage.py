import logging

from flask_fixtures import load_fixtures_from_file
from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app
from src.models import db

logger = logging.getLogger(__name__)

manager = Manager(create_app)


def loan_fixtures(fixtures):
    for fixture in fixtures:
        load_fixtures_from_file(db=db, fixture_filename=f"src/fixtures/{fixture}.json")


@manager.option(dest="fixture")
def load_db(fixture):
    if fixture == "all":
        loan_fixtures(["location", "genres", "artists", "venues", "shows"])
    else:
        loan_fixtures([fixture])


manager.add_command("db", MigrateCommand)
manager.run()
