"""
config.py

Different configurations for the application based on the different
run environments (development and production).
"""
import os

project_dir = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """
    Common configurations.
    """
    JWT_ACCESS_LIFESPAN = {'hours': 24}
    JWT_ACCESS_REFRESH = {'days': 30}

    SECRET_KEY = os.urandom(32)

    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
        os.path.join(project_dir, "dev.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    Development-specific configurations.
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production-specific configurations.
    """
    DEBUG = False
    TESTING = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
