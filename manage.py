import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
from app.models.users import User
from app.models.flashcard_collections import FlashcardCollection
from app.models.category import Category
from app.models.flashcard import Flashcard
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, FlashcardCollection=FlashcardCollection, \
                Category=Category, Flashcard=Flashcard)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    """Run deployment task"""
    from flask_migrate import migrate, upgrade, init

    # init database
    init()

    # create migrations
    migrate()

    # update Database
    upgrade()


if __name__ == '__main__':
    manager.run()
