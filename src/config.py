import os


class Config:
    DEBUG = False
    TESTING = False

    TEST_AUTO_LOGIN = False

    LOAD_VIEWS = os.environ.get('LOAD_VIEWS', True)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY'
    NSSL_SERVER_URL = os.environ.get('NSSL_SERVER_URL')


class ProductionConfig(Config):
    pass


class DevelopConfig(Config):
    DEBUG = True

    TEST_AUTO_LOGIN = os.environ.get('TEST_AUTO_LOGIN', False)
    AUTO_LOGIN_USER = os.environ.get('AUTO_LOGIN_USER', None)
    AUTO_LOGIN_PASSWORD = os.environ.get('AUTO_LOGIN_PASSWORD', None)


class TestConfig(DevelopConfig):
    TESTING = True
    DEBUG = False

    WTF_CSRF_ENABLED = False

    TEST_SHOPPING_LIST_NAME = "WebTestList"
    NSSL_SERVER_URL = "https://nssl.susch.eu"
    TEST_USER = "Testtest"
    TEST_USER_PASSWORD = "test"
