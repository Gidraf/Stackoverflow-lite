import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False

test_params={
"host":"localhost",
"database":"test",
"user":"postgres",
"password":""
}

iparams={
"host":"localhost",
"database":"stackoverflow",
"user":"postgres",
"password":""
}

params={
"host":"ec2-54-225-76-201.compute-1.amazonaws.com",
"database":"d8d0a31kom78qc",
"user":"tpymuqbzuqpntj",
"password":"ee673df3c0c88bd0b0c278a5df066d89be40c079a5b7dd794f3ad3cb36cfc3bf"
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
