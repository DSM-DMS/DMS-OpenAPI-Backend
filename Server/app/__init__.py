from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger

from mongoengine import connect

from app.views import *

WEB_FILE_ROOT_DIR = '../web_files'


def create_app(*config_cls):
    print('[INFO] Flask application initialized with {}'.format([config.__name__ for config in config_cls]))

    app_ = Flask(
        __name__,
        static_folder='{}/static'.format(WEB_FILE_ROOT_DIR),
        template_folder='{}/templates'.format(WEB_FILE_ROOT_DIR)
    )

    for config in config_cls:
        app_.config.from_object(config)

    connect(**app_.config['MONGODB_SETTINGS'])

    cfg = app_.config

    JWTManager().init_app(app_)
    CORS().init_app(app_)
    Swagger(template=app_.config['SWAGGER_TEMPLATE']).init_app(app_)

    Router().init_app(app_)

    app_.after_request(after_request)
    app_.register_error_handler(Exception, exception_handler)

    return app_
