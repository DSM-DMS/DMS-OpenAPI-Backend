from bson.objectid import ObjectId
from datetime import datetime

from mongoengine import *


class PointHistoryModel(EmbeddedDocument):
    """
    각 학생에게 속해 있는(Embedded) 상벌점 내역
    """
    meta = {
        'collection': 'point_history'
    }

    id = ObjectIdField(
        primary_key=True,
        default=ObjectId
    )

    time = DateTimeField(
        default=datetime.now
    )
    # 상벌점을 부과한 시간

    reason = StringField(
        required=True
    )
    # 벌점 부과 사유

    point_type = BooleanField(
        required=True
    )
    # True : 상점, False : 벌점

    point = IntField(
        required=True
    )
    # 부과한 점수
