import os, sys
from pathlib import Path

BASE_DIR = str(Path(__file__).resolve().parent.parent)
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from main import create_app, db
from main.models import user, member


app = create_app(os.getenv('FLASK_ENV') or 'dev')
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db, compare_type=True, render_as_batch=True)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()