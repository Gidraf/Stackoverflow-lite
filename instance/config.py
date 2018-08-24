import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False

params={
"host":"localhost",
"database":"test",
"user":"postgres",
"password":"postgres"
}

secrets='d3b5c6e30af8a9c65c41a683ff22f382489df6a061663379'
class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
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
