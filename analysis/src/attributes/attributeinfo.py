from mongoengine import (
     DictField, ListField, StringField, DecimalField, IntField, MapField,
     DateTimeField, URLField, EmbeddedDocument, EmbeddedDocumentField, 
     DynamicDocument)

from parsing import ParsedProduct


class AttrValueStats(EmbeddedDocument):
    count = IntField()
    mean_price = DecimalField()
    median_price = DecimalField()
    mean_rating = DecimalField()
    median_rating = DecimalField()


class AttrStats(EmbeddedDocument):
    count = IntField()
    values = DictField()


class AttrInfo(DynamicDocument):
    name = StringField()
    rank = IntField()
    stats = AttrStats()
    meta = {'allow_inheritance': True}


#def sum_func(obj, prev):
#    


if __name__ == "__main__":
    #prods = ParsedProduct.objects.select_related()

    use_attrs = ['tvType', 'screenSizeIn']

    rank = 1
    for cur_attr in use_attrs:
        full_attr_str = "attr.{0}".format(cur_attr)
        #exist_set = ParsedProduct.objects(full_attr_str__exists=True)
        
        #values = ParsedProduct.objects.distinct(full_attr_str)
        #values = ParsedProduct.objects(attr.tvType__exists=True).distinct(field=attr.tvType)
        
        print "distinct values: {0}".format(values)

        new_ai = AttrInfo()
        new_ai.name = cur_attr
        new_ai.rank = rank
        rank = rank + 1

        new_ai.stats = AttrStats()
        new_ai.stats.count = prods.count({full_attr_str: {"$exists": True}})

        for val in values:
            avs = AttrValueStats()
            avs.count = prods.count({full_attr_str: val})
            #sum_price = prods.group({key: {regularPrice: True},
            #                         cond: {full_attr_str: val},
            #                         reduce: function()
            #                          )
            new_ai.stats.values[val] = avs

    pass