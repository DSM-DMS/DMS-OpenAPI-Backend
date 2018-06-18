from app.docs import SAMPLE_OBJECT_IDS, jwt_header, secret_key_header

POST_LIST_GET = {
    'tags': ['게시글'],
    'description': '게시글 리스트를 조회합니다.',
    'parameters': [
        jwt_header,
        secret_key_header
    ],
    'responses': {
        '200': {
            'description': '게시글 리스트 조회 성공',
            'examples': {
                '': [
                    {
                        'id': SAMPLE_OBJECT_IDS[0],
                        'writeTime': '2017-10-11',
                        'author': '교촌치킨',
                        'title': '치킨 먹는법',
                        'pinned': True
                    },
                    {
                        'id': SAMPLE_OBJECT_IDS[1],
                        'writeTime': '2017-10-13',
                        'author': '코레일',
                        'title': 'KTX 싸게 예매하는법',
                        'pinned': False
                    },
                    {
                        'id': SAMPLE_OBJECT_IDS[2],
                        'writeTime': '2017-10-16',
                        'author': '갓석진',
                        'title': '서울에서 먹고살기',
                        'pinned': False
                    }
                ]
            }
        },
        '403': {
            'description': '권한 없음'
        }
    }
}

POST_ITEM_GET = {
    'tags': ['게시글'],
    'description': '특정 게시글의 내용을 조회합니다.',
    'parameters': [
        jwt_header,
        secret_key_header,
        {
            'name': 'post_id',
            'description': '조회할 게시글의 ID',
            'in': 'path',
            'type': 'str',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': 'FAQ 조회 성공',
            'examples': {
                '': {
                    'writeTime': '2017-10-11',
                    'author': '교촌치킨',
                    'title': '치킨 먹는법',
                    'content': '교촌허니콤보를 웨지감자와 함께',
                    'pinned': True
                }
            }
        },
        '204': {
            'description': '게시글 조회 실패(존재하지 않는 ID)'
        },
        '403': {
            'description': '권한 없음'
        }
    }
}
