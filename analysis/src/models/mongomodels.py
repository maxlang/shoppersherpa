from mongoengine import DynamicDocument, DictField


class Product(DynamicDocument):
    attr = DictField()
    meta = {'allow_inheritance': True}

