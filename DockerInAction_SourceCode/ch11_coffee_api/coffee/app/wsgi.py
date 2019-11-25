import os

from . import create_app

app = create_app(os.getenv('COFFEEFINDER_CONFIG') or 'default')
