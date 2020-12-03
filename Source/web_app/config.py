import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """base configuration class for this web application"""
    SECRET_KEY = os.environ.get('PROJECT5_FLASK_APP_SECRET_KEY')
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.google.com")
    MAIL_PORT = os.environ.get("MAIL_PORT",587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS",True)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_SUBJECT_PREFIX = "[Metis Project 5]"
    PROJ5_EMAIL_SENDER = os.environ.get("PROJ5_EMAIL_SENDER")
    PROJ5_ADMIN = os.environ.get("PROJ5_ADMIN")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    
    DEBUG = True
    
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DATABASE_NAME = os.environ.get('DEV_DATABASE_NAME')
    DB_URI = 'mysql+pymysql://%s:%s@%s:3306/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)

    SQLALCHEMY_DATABASE_URI = DB_URI

class TestConfig(Config):
    TESTING = True
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DATABASE_NAME = os.environ.get('TEST_DATABASE_NAME')
    DB_URI = 'mysql+pymysql://%s:%s@%s:3306/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)
    
    SQLALCHEMY_DATABASE_URI = DB_URI

class ProductionConfig(Config):

    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DATABASE_NAME = os.environ.get('DATABASE_NAME')
    DB_URI = 'mysql+pymysql://%s:%s@%s:3306/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)

    SQLALCHEMY_DATABASE_URI = DB_URI    
    

config = {
    "development" : DevelopmentConfig,
    "testing" : TestConfig,
    "production" : ProductionConfig,
    "default" : DevelopmentConfig
}
