from datetime import datetime
from uuid import uuid4

from mongoengine import *


class AccountBase(Document):
    """
    계정에 대한 상위 collection
    """
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    signup_time = DateTimeField(
        default=datetime.now
    )
    # 회원가입 시간

    id = StringField(
        primary_key=True
    )
    pw = StringField(
        required=True
    )
    name = StringField(
        required=True
    )


class StudentModel(AccountBase):
    meta = {
        'collection': 'account_student'
    }

    number = IntField(
        required=True,
        min_value=1101,
        max_value=3421
    )

    good_point = IntField(
        default=0
    )
    # 상점

    bad_point = IntField(
        default=0
    )
    # 벌점

    point_histories = EmbeddedDocumentListField(
        document_type='PointHistoryModel'
    )
    # 상벌점 내역

    penalty_training_status = BooleanField(
        default=False
    )
    # 벌점 교육 중인지의 여부

    penalty_level = IntField(
        default=0
    )
    # 벌점 교육 단계


class TokenModel(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    owner = ReferenceField(
        document_type='AccountBase',
        required=True,
        reverse_delete_rule=CASCADE,
        unique_with='user_agent'
    )

    user_agent = StringField(
        required=True
    )

    identity = UUIDField(
        unique=True
    )

    @classmethod
    def generate_token(cls, model, owner, user_agent):
        while True:
            uuid = uuid4()

            if not model.objects(identity=uuid):
                model.objects(owner=owner, user_agent=user_agent).delete()

                params = {
                    'owner': owner,
                    'user_agent': user_agent,
                    'identity': uuid
                }

                if model is RefreshTokenModel:
                    params['pw_snapshot'] = owner.pw

                model(**params).save()

                return str(uuid)


class AccessTokenModel(TokenModel):
    meta = {
        'collection': 'access_token_open_api'
    }


class RefreshTokenModel(TokenModel):
    """
    JWT refresh token을 관리하기 위한 collection
    """
    meta = {
        'collection': 'refresh_token_open_api'
    }

    pw_snapshot = StringField(
        required=True
    )
    # Refresh token 발급 당시의 비밀번호
