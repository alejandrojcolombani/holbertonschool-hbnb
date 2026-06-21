import os


class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')


class TestingConfig(DevelopmentConfig):
    TESTING = True
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
