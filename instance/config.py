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
"host":"ec2-54-83-50-145.compute-1.amazonaws.com",
"database":"defja9o5949ule",
"user":"idaouwllvozqis",
"password":"80ae8fb0ed1f164bbe69f4954c43897c2e9ffe83b712d8344cd035416f5abee7"
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
