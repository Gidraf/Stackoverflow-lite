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
"host":"ec2-174-129-35-61.compute-1.amazonaws.com",
"database":"d52h1cvi93s8ea",
"user":"eehfjmsffbxqln",
"password":"7d442b7ff360c6bca04ed0b84798541706d134fddd2a60982d2d21d227601f54"
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
