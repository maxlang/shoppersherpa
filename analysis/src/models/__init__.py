from mongoengine import connect
from models.mongomodels import Product

db = 'test'

connect(db)

print 'models loaded'
