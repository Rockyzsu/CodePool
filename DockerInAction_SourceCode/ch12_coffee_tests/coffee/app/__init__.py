from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    import errors
    from api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

