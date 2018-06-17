from datetime import timedelta
import os


class Config:
    SERVICE_NAME = 'DMS-OpenAPI'
    DB_NAME = 'dms-v2'
    SERVICE_NAME_UPPER = SERVICE_NAME.upper()
    REPRESENTATIVE_HOST = 'dsm2015.cafe24.com/open-api'

    RUN_SETTING = {
        'threaded': True
    }

    SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')
    # Secret key for any 3-rd party libraries

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_HEADER_TYPE = 'JWT'

    MONGODB_SETTINGS = {
        'db': DB_NAME,
        'host': None,
        'port': None,
        'username': os.getenv('MONGO_ID'),
        'password': os.getenv('MONGO_PW')
    }

    SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

    SWAGGER = {
        'title': SERVICE_NAME,
        'specs_route': os.getenv('SWAGGER_URI', '/docs'),
        'uiversion': 3,

        'info': {
            'title': SERVICE_NAME,
            'version': '1.0',
            'description': ''
        },
        'basePath': '/'
    }

    SWAGGER_TEMPLATE = {
        'schemes': [
            'http'
        ],
        'tags': [
            {
                'name': 'JWT 관련',
                'description': '로그인 상태 체크, Access token refresh 등 JWT 관련 API'
            },
            {
                'name': '게시글',
                'description': '로그인된 계정 권한으로 접근 가능한 게시글 API'
            },
            {
                'name': '학교 정보',
                'description': '학교 정보 API'
            },

            {
                'name': '계정',
                'description': '학생 계정 관련 API'
            },
            {
                'name': '계정 관리',
                'description': '학생 계정으로 접근 가능한 계정 관리 API'
            },
            {
                'name': '소셜 계정',
                'description': '학생 소셜 계정 관련 API'
            },
            {
                'name': '신청',
                'description': '학생 신청 관련 API'
            },
            {
                'name': '신고',
                'description': '학생 신고 관련 API'
            }
        ]
    }
