from mongoengine import connect, DynamicDocument, DictField
import mongoengine

db = 'test'

connect(db)

dbName = 'test'

connect(dbName)


class Product(DynamicDocument):
    attr = DictField()
    meta = {'allow_inheritance': True}

print 'models loaded'
