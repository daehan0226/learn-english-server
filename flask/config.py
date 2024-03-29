import os
from dotenv import load_dotenv


APP_ROOT = os.path.join(os.path.dirname(__file__), "..")
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)


class Config:
    """https://flask.palletsprojects.com/en/2.0.x/config"""

    TESTING = False
    DEBUG = False
    ENV = "development"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SSH_HOST = os.getenv("SSH_HOST")
    SSH_PORT = os.getenv("SSH_PORT")
    SSH_USER = os.getenv("SSH_USER")
    SSH_PASSWORD = os.getenv("SSH_PASSWORD")
    CRAWLER = os.getenv("CRAWLER")


class ProductionConfig(Config):
    ENV = "production"
    HOST = os.getenv("APP_HOST_PROD")
    PORT = os.getenv("APP_PORT_PROD")
    db_url = f'mysql+pymysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@{os.getenv("MYSQL")}:{os.getenv("MYSQL_PORT")}/{os.getenv("MYSQL_DATABASE")}'
    SQLALCHEMY_DATABASE_URI = db_url
    MONGO_URI = os.getenv("MONGO_DB_URI_PROD")
    REDIS_URL = f'redis://:{os.getenv("REDIS_PASSWORD")}@{os.getenv("REDIS")}:{os.getenv("REDIS_PORT")}/0'


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = os.getenv("APP_HOST_DEV")
    PORT = os.getenv("APP_PORT_DEV")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI_DEV")
    MONGO_URI = os.getenv("MONGO_DB_URI_DEV")
    REDIS_URL = os.getenv("REDIS_URL_DEV")


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI_TEST")
    MONGO_URI = os.getenv("MONGO_DB_URI_DEV")
    REDIS_URL = os.getenv("REDIS_URL_DEV")


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)
