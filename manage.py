import os
import unittest
import uuid
from flask_script import Manager, Shell, Command
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
# from app.models import User, Role, APIKey
from sharedmodels.models import User, Role, APIKey


class InitDB(Command):
    def run(self):
        db.drop_all()
        db.create_all()

        # data object
        user1 = User(username='luowanqian', password='123')
        user2 = User(username='admin', password='123')
        apikey1 = APIKey(application='Face Detect',
                         apikey=str(uuid.uuid1()), user=user1)
        apikey2 = APIKey(application='Face Recognition',
                         apikey=str(uuid.uuid1()), user=user1)
        apikey3 = APIKey(application='Face Compare',
                         apikey=str(uuid.uuid1()), user=user2)

        # commit to database
        db.session.add_all([user1, user2, apikey1, apikey2, apikey3])
        db.session.commit()


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('initdb', InitDB())


@manager.command
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
