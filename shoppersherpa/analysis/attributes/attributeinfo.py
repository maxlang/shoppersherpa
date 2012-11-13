from mongoengine import (
     DictField, ListField, StringField, DecimalField, IntField, MapField,
     BooleanField, DateTimeField, URLField, EmbeddedDocument,
     EmbeddedDocumentField, DynamicDocument)

from models.models import (ParsedProduct, AttrInfo)
import numpy
#from shoppersherpa.models import ParsedProduct


class AttrValueStats(EmbeddedDocument):
    count = IntField()
    mean_price = DecimalField()
    median_price = DecimalField()
    mean_rating = DecimalField()
    median_rating = DecimalField()
    price_std_dev = DecimalField()
    rating_std_dev = DecimalField()


class AttrStats(EmbeddedDocument):
    count = IntField()
    values = DictField()
    

def sum_field(doc_set, field):
    total = 0
    for d in doc_set:
        attr = d['attr']
        if field in attr:
            total += attr[field]
    return total


def convert_to_vector(doc_set, field):
    ls = []
    for prod in doc_set:
        attr = prod['attr']
        if field in attr and attr[field] is not None:
            ls.append(attr[field])
    return numpy.array([ls])


def find_median(doc_set, field):
    vals = [x['attr'][field] for x in doc_set]
    vals.sort()
    if len(vals) == 0:
        return None
    elif len(vals) % 1 == 1:
        return vals[len(vals) / 2]
    else:
        return (vals[(len(vals) / 2) - 1] + vals[(len(vals) / 2)]) / 2


if __name__ == "__main__":
    print 'deleting'
    AttrInfo.objects.delete()

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
            price_vec = convert_to_vector(ParsedProduct.objects(**{filter_attr_str: val}), 'regularPrice')
            rating_vec = convert_to_vector(ParsedProduct.objects(**{filter_attr_str: val}), 'customerReviewAverage')
            cutoff_rating_vec = convert_to_vector(ParsedProduct.objects(
                                                                        **{filter_attr_str: val, 
                                                                           'customerReviewCount': {"$gte": 10}}), 
                                                  'customerReviewAverage')
            #rating_vec = price_vec
            avs.count = len(price_vec)

            avs.mean_price = numpy.mean(price_vec)
            avs.median_price = numpy.median(price_vec)
            avs.mean_rating = numpy.mean(rating_vec)
            avs.median_rating = numpy.median(rating_vec)
            avs.price_std_dev = numpy.std(price_vec)
            avs.rating_std_dev = numpy.std(rating_vec)

            print "{6}: {0} {1} {2} {3} {4} {5}".format(avs.mean_price,
                                                        avs.median_price,
                                                        avs.mean_rating,
                                                        avs.median_rating,
                                                        avs.price_std_dev,
                                                        avs.rating_std_dev,
                                                        val)

            new_ai.stats.values[val] = avs
            new_ai.save()

            print "{0} {1}".format(val, new_ai.stats.values[val].count)

    pass