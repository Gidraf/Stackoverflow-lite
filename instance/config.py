import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False


params={
"host":os.environ["LOCALHOST"],
"database":os.environ["DATABASE"],
"user":os.environ["USERNAME"],
"password":os.environ["PASSWORD"]
}

secrets = os.environ["SECRETS"]

class DevelopmentConfig(Config):
    """
    Configurations for Development
    """
    DEBUG = True

class TestingConfig(Config):
    """
    Configurations for Testing, with a separate test database.
    """
    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig
}
