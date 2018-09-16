from mongoengine import StringField, IntField, Document

class Stats(Document):
    negative = IntField(default=0)
    positive = IntField(default=0)

class Word(Document):
    word = StringField(required=True, unique=True)
    positive = IntField(default=0)
    negative = IntField(default=0)
    meta = {
        'indexes': [
            '$word',
        ]
    }