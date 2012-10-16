import mongoengine
from mongoengine import *

# TODO move this to config files
dbName = 'test'

connect(dbName)

class Product(DynamicDocument):
    pass


'''
# information about data providers - either retailers or manufacturers
class Provider(DynamicDocument):
    name = StringField()
    url = URLField()

## DATA

class Price(DynamicEmbeddedDocument):
    amount = DecimalField()
    currency = StringField(choices=('USD'))

class Attribute(DynamicEmbeddedDocument):
    name = StringField()
    value = DynamicField()

class Source(DynamicEmbeddedDocument):
    provider = ReferenceField(Provider, dbref=False)
    url = URLField()

class Condition(DynamicEmbeddedDocument):
    name = StringField()

class Identifier(DynamicEmbeddedDocument):
    type = StringField()
    value = StringField()

class ShippingOption(DynamicEmbeddedDocument):
    name = StringField()
    price = EmbeddedDocumentField(Price)

class Review(DynamicEmbeddedDocument):
    pass

class Warranty(DynamicEmbeddedDocument):
    pass

class HistoryPointer(EmbeddedDocument):
    lastgood = DateTimeField()

## METADATA

class SourceData(DynamicEmbeddedDocument):
    list = ListField(EmbeddedDocumentField(Source))
    
class ReviewData(DynamicEmbeddedDocument):
    list = ListField(EmbeddedDocumentField(Review))
    count = IntField()
    average = DecimalField()

class IdentifierData(DynamicEmbeddedDocument):
    list = ListField(EmbeddedDocumentField(Identifier))

class AttributeData(DynamicEmbeddedDocument):
    list = ListField(EmbeddedDocumentField(Attribute))

class AvailabilityData(DynamicEmbeddedDocument):
    pass

class TaxData(DynamicEmbeddedDocument):
    pass
    
class ShippingData(DynamicEmbeddedDocument):
    options = ListField(EmbeddedDocumentField(ShippingOption))   

class class WarrantyData(DynamicEmbeddedDocument):
    options = ListField(EmbeddedDocumentField(Warranty))   

## DATA COLLECTIONS

class PriceData(DynamicEmbeddedDocument):
    base = EmbeddedDocumentField(Price)
    tax = EmbeddedDocumentField(TaxData)
    shipping = EmbeddedDocumentField(ShippingData)
    warranty = EmbeddedDocumentField(WarrantyData)

class OfferSnapshot(DynamicEmbeddedDocument):
    datetime = DateTimeField()
    prices = GenericEmbeddedDocumentField(choices=(PriceData,HistoryPointer))
    availability = GenericEmbeddedDocumentField(choices=(AvailabilityData,HistoryPointer))
    attributes = GenericEmbeddedDocumentField(choices=(AttributeData,HistoryPointer))

class Offer(DynamicEmbeddedDocument):
    source = EmbeddedDocumentField(Source)
    identifiers = EmbeddedDocumentField(IdentifierData)
    condition = StringField(choices=('New','Used'))
    price = EmbeddedDocumentField(PriceData)
    availability = EmbeddedDocumentField(AvailabilityData)
    attributes = EmbeddedDocumentField(AttributeData)
    history = ListField(EmbeddedDocumentField(OfferSnapshot))

class OfferData(DynamicEmbeddedDocument):
    list = ListField(EmbeddedDocumentField(Offer))

# Basic product class for storing product information
class Product(DynamicDocument):
    attributes = EmbeddedDocumentField(AttributeData)
    offers = EmbeddedDocumentField(OfferData)
    reviews = EmbeddedDocumentField(ReviewData)
    sources = EmbeddedDocumentField(SourceData)
    identifiers = EmbeddedDocumentField(IdentifierData)
    warranty = EmbeddedDocumentField(WarrantyData)
'''
print 'loaded model'
