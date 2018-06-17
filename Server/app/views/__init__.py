from binascii import hexlify
from hashlib import pbkdf2_hmac
from uuid import UUID

from functools import wraps
import gzip
import ujson
import time

from flask import Response, abort, after_this_request, current_app, g, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app.models.account import AccessTokenModel, AdminModel, StudentModel


def auth_required(model):
    def decorator(fn):
        @wraps(fn)
        @jwt_required
        def wrapper(*args, **kwargs):
            try:
                token = AccessTokenModel.objects(identity=UUID(get_jwt_identity())).first()

                if not token or not isinstance(token.owner, model):
                    abort(403)

                g.user = token.owner

                return fn(*args, **kwargs)
            except ValueError:
                abort(422)
        return wrapper
    return decorator


def gzipped(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        @after_this_request
        def zipper(response):
            if 'gzip' not in request.headers.get('Accept-Encoding', '')\
                    or not 200 <= response.status_code < 300\
                    or 'Content-Encoding' in response.headers:
                # 1. Accept-Encoding에 gzip이 포함되어 있지 않거나
                # 2. 200번대의 status code로 response하지 않거나
                # 3. response header에 이미 Content-Encoding이 명시되어 있는 경우
                return response

            response.data = gzip.compress(response.data)
            response.headers.update({
                'Content-Encoding': 'gzip',
                'Vary': 'Accept-Encoding',
                'Content-Length': len(response.data)
            })

            return response
        return fn(*args, **kwargs)
    return wrapper


def json_required(required_keys):
    def decorator(fn):
        if fn.__name__ == 'get':
            print('[WARN] JSON with GET method? on "{}()"'.format(fn.__qualname__))

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                abort(406)

            for key, typ in required_keys.items():
                if key not in request.json or type(request.json[key]) is not typ:
                    abort(400)
                if typ is str and not request.json[key]:
                    abort(400)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


class BaseResource(Resource):
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def unicode_safe_json_dumps(cls, data, status_code=200, **kwargs):
        return Response(
            ujson.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )

    @classmethod
    def encrypt_password(cls, password):
        return hexlify(pbkdf2_hmac(
            hash_name='sha256',
            password=password.encode(),
            salt=current_app.secret_key.encode(),
            iterations=100000
        )).decode('utf-8')

    class ValidationError(Exception):
        def __init__(self, description='', *args):
            self.description = description

            super(BaseResource.ValidationError, self).__init__(*args)


def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'deny'

    return response


def exception_handler(e):
    print(e)

    if isinstance(e, HTTPException):
        description = e.description
        code = e.code
    elif isinstance(e, BaseResource.ValidationError):
        description = e.description
        code = 400
    else:
        description = ''
        code = 500

    return jsonify({
        'msg': description
    }), code


class Router:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    @classmethod
    def add_prefix(cls, api):
        if not api.prefix.startswith('/open-api'):
            api.prefix = '/{}{}'.format('open-api', api.prefix)

        return api

    def init_app(self, app):
        from .jwt import checker, refresh
        app.register_blueprint(self.add_prefix(checker.api).blueprint)
        app.register_blueprint(self.add_prefix(refresh.api).blueprint)

        from .metadata import developers, links, version
        app.register_blueprint(self.add_prefix(developers.api).blueprint)
        app.register_blueprint(self.add_prefix(links.api).blueprint)
        app.register_blueprint(self.add_prefix(version.api).blueprint)

        from .post import post, preview
        app.register_blueprint(self.add_prefix(post.api).blueprint)
        app.register_blueprint(self.add_prefix(preview.api).blueprint)

        from .school_data import meal
        app.register_blueprint(self.add_prefix(meal.api).blueprint)

        from .account import alteration, auth, info, signup, social_auth
        app.register_blueprint(self.add_prefix(alteration.api).blueprint)
        app.register_blueprint(self.add_prefix(auth.api).blueprint)
        app.register_blueprint(self.add_prefix(info.api).blueprint)
        app.register_blueprint(self.add_prefix(signup.api).blueprint)
        app.register_blueprint(self.add_prefix(social_auth.api).blueprint)

        from .apply import extension, goingout, stay
        app.register_blueprint(self.add_prefix(extension.api).blueprint)
        app.register_blueprint(self.add_prefix(goingout.api).blueprint)
        app.register_blueprint(self.add_prefix(stay.api).blueprint)

        from .report import facility_report, bug_report
        app.register_blueprint(self.add_prefix(facility_report.api).blueprint)
        app.register_blueprint(self.add_prefix(bug_report.api).blueprint)
