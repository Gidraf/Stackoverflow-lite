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
"host":"ec2-54-235-94-36.compute-1.amazonaws.com",
"database":"d5o5i73sh1j53r",
"user":"iokukimlnkbwhw",
"password":"6ee53e98f42d9d1bae340ea3b0ac22a335d5010d9610cd5dd0d1acffc1a307d4"
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
