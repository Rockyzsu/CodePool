import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('COFFEEFINDER_DB_URI')
    if SQLALCHEMY_DATABASE_URI is None or SQLALCHEMY_DATABASE_URI == '':
        raise Exception('COFFEEFINDER_DB_URI environment variable must be specified.')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
