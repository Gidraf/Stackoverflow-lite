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

params={
"host":"localhost",
"database":"stackoverflow",
"user":"postgres",
"password":""
}

iparams={
"host":"ec2-54-83-51-78.compute-1.amazonaws.com",
"database":"daujh8hhpq4mnl",
"user":"rkagydzqgpygvd",
"password":"704f8afcc2d6187d7726c931bcfd1d7475392b562577c7d9222ef119c58bbc42"
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
