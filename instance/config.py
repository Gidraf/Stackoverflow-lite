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
"host":"ec2-54-83-27-165.compute-1.amazonaws.com",
"database":"db1lqjl8v56lo4",
"user":"mggoditggdcyqf",
"password":"e2687527460c8aa5a24b0c1de48792b96f78e59a3058092557fc223f49e06e8a"
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
