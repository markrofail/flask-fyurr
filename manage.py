from flask_fixtures import load_fixtures_from_file
from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app
from src.models import db

manager = Manager(create_app)


@manager.command
def seed():
    fixtures = ["artists.json", "venues.json", "shows.json"]
    for fixture in fixtures:
        load_fixtures_from_file(db=db, fixture_filename=f"src/fixtures/{fixture}")


manager.add_command("db", MigrateCommand)
manager.run()
