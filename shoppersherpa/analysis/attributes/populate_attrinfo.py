from shoppersherpa.models.models import (AttrInfo, Product)
#from shoppersherpa.models import ParsedProduct


def fallbackNormalize(prod, attrlist):
    for x in attrlist:
        if x in prod.attr:
            return prod.attr[x]

    return None


def normalize3d(prod):
    name = prod.attr['name'].lower()
    return "3d" in name

if __name__ == "__main__":
    size_ai = AttrInfo()
    size_ai.name = "size"
    size_ai.display_name = "Screen Size"
    size_ai.is_discrete = False
    size_ai.is_independant = True
    size_ai.rank = 1
    size_ai.units = "inches"

    brand_ai = AttrInfo()
    brand_ai.name = "brand"
    brand_ai.display_name = "Brand"
    brand_ai.is_discrete = True
    brand_ai.is_independant = True
    brand_ai.rank = 2
    brand_ai.units = None

    tv_type_ai = AttrInfo()
    tv_type_ai.name = "tv_type"
    tv_type_ai.display_name = "Television Type"
    tv_type_ai.is_discrete = True
    tv_type_ai.is_independant = True
    tv_type_ai.rank = 3
    tv_type_ai.units = None

    res_ai = AttrInfo()
    res_ai.name = "resolution"
    res_ai.display_name = "Resolution"
    res_ai.is_discrete = True
    res_ai.is_independant = True
    res_ai.rank = 4
    res_ai.units = None

    refresh_ai = AttrInfo()
    refresh_ai.name = "refresh"
    refresh_ai.display_name = "Refresh Rate"
    refresh_ai.is_discrete = True
    refresh_ai.is_independant = True
    refresh_ai.rank = 5
    refresh_ai.units = "Hertz"

    is_3d_ai = AttrInfo()
    is_3d_ai.name = "is_3d"
    is_3d_ai.display_name = "Supports 3D"
    is_3d_ai.is_discrete = True
    is_3d_ai.is_independant = True
    is_3d_ai.rank = 6
    is_3d_ai.units = None

    color_ai = AttrInfo()
    color_ai.name = "color"
    color_ai.display_name = "Color"
    color_ai.is_discrete = True
    color_ai.is_independant = True
    color_ai.units = None
    color_ai.rank = 7

    num_rating_ai = AttrInfo()
    num_rating_ai.name = "ratings_num"
    num_rating_ai.display_name = "Number of Ratings"
    num_rating_ai.is_discrete = False
    num_rating_ai.is_independant = False
    num_rating_ai.units = None
    num_rating_ai.rank = None

    avg_rating_ai = AttrInfo()
    avg_rating_ai.name = "ratings_avg"
    avg_rating_ai.display_name = "Average Ratings"
    avg_rating_ai.is_discrete = False
    avg_rating_ai.is_independant = False
    avg_rating_ai.units = None
    avg_rating_ai.rank = None

    price_ai = AttrInfo()
    price_ai.name = "price"
    price_ai.display_name = "Price"
    price_ai.is_discrete = False
    price_ai.is_independant = False
    price_ai.units = None
    price_ai.rank = None


    ai_elements = [(size_ai, lambda x: fallbackNormalize(x, ['screenSizeIn', 'screenSizeClassIn'])),
                   (brand_ai, lambda x: fallbackNormalize(x, ['manufacturer'])),
                   (tv_type_ai, lambda x: fallbackNormalize(x, ['tvType'])),
                   (res_ai, lambda x: fallbackNormalize(x, ['verticalResolution'])),
                   (refresh_ai, lambda x: fallbackNormalize(x, ['screenRefreshRateHz'])),
                   (is_3d_ai, normalize3d),
                   (color_ai, lambda x: fallbackNormalize(x, ['color'])),
                   (num_rating_ai, lambda x: fallbackNormalize(x, ['customerReviewCount'])),
                   (avg_rating_ai, lambda x: fallbackNormalize(x, ['customerReviewAverage'])),
                   (price_ai, lambda x: fallbackNormalize(x, ['regularPrice']))]

    AttrInfo.objects.delete()
    print ("cleared AttrInfo table")
    #Product.objects.selectRelated()

    for prod in Product.objects:

        for ai_tup in ai_elements:
            ai = ai_tup[0]
            norm_func = ai_tup[1]

            prod.normalized[ai.name] = norm_func(prod)
        prod.save()

    print("normalized products")

    for ai_tup in ai_elements:
        ai = ai_tup[0]
        vals = filter(lambda x: x is not None,
                      Product.objects.distinct("normalized.{0}".format(ai.name)))
        #vals.sort()
        ai.values = vals
        ai.save()

    print ("saved attribute meta data")
