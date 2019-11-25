import os

from app import create_app, db
from app.model import CoffeeShop
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('COFFEEFINDER_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, CoffeeShop=CoffeeShop)
    manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def create_tables():
    """Create the database tables."""
    db.create_all()

if __name__ == '__main__':
    manager.run()
