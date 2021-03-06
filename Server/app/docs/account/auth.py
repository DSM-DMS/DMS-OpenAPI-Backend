from app.docs import SAMPLE_ACCESS_TOKEN, SAMPLE_REFRESH_TOKEN, secret_key_header

AUTH_POST = {
    'tags': ['[Student] 계정'],
    'description': '로그인',
    'parameters': [
        secret_key_header,
        {
            'name': 'id',
            'description': 'ID',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'password',
            'description': '비밀번호',
            'in': 'json',
            'type': 'str',
            'required': True
        }
    ],
    'responses': {
        '201': {
            'description': '로그인 성공',
            'examples': {
                '': {
                    'accessToken': SAMPLE_ACCESS_TOKEN,
                    'refreshToken': SAMPLE_REFRESH_TOKEN
                }
            }
        },
        '401': {
            'description': '로그인 실패'
        }
    }
}
