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

def sum_field(doc_set, field):
    total = 0
    for d in doc_set:
        attr = d['attr']
        if field in attr:
            total += attr[field]
            
def find_median(doc_set, field):
    vals = [x['attr'][field] for x in doc_set]
    vals.sort()


if __name__ == "__main__":
    #prods = ParsedProduct.objects.select_related()
    #prods = ParsedProduct.objects

    use_attrs = ['tvType', 'screenSizeIn']

    rank = 1
    for cur_attr in use_attrs:
        full_attr_str = "attr.{0}".format(cur_attr)
        filter_attr_str = "attr__{0}".format(cur_attr)
        values = ParsedProduct.objects.distinct(full_attr_str)

        print "distinct values: {0}".format(values)

        new_ai = AttrInfo()
        new_ai.name = cur_attr
        new_ai.rank = rank
        rank = rank + 1

        new_ai.stats = AttrStats()
        new_ai.stats.count = ParsedProduct.objects(**{filter_attr_str: {"$exists": True}}).count()
        print new_ai.stats.count

        for val in values:
            avs = AttrValueStats()
            val_set = ParsedProduct.objects(**{filter_attr_str: val})
            avs.count = val_set.count()
            #sum_price = ParsedProduct.objects.group({key: {"regularPrice": True},
            #                         cond: {full_attr_str: val},
            #                         reduce: function()
            #                          )
            avs.mean_price = sum_field(val_set, 'regularPrice') / avs.count
            
            new_ai.stats.values[val] = avs

            #map_func = "function() {emit('xx', this.regularPrice)}"
            #reduce_func = "function(key, values) {var sum=0; for (var i=0; i<values. length; i++) {sum += values[i];} return sum;}"
            #ParsedProduct.objects.map_reduce(map_func, reduce_func, output='mapreduceout')


            print "{0} {1}".format(val, new_ai.stats.values[val].count)

    pass