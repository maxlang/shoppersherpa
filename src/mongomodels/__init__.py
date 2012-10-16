from mongoengine import *
import mongoengine

db = 'test'

connect(db)

dbName = 'test'

connect(dbName)

class Product(DynamicDocument):
    attr = DictField()
    
print 'models loaded'