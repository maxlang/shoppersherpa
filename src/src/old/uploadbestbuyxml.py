from pymongo import Connection
from xml.dom.minidom import parseString

connection = Connection('localhost', 27017)

db = connection['test']

products_col = db['products']

filenames = (r"C:\code\shoppersherpa\bestbuyxml\bbxml1.xml",
             r"C:\code\shoppersherpa\bestbuyxml\bbxml2.xml",
             r"C:\code\shoppersherpa\bestbuyxml\bbxml3.xml",
             r"C:\code\shoppersherpa\bestbuyxml\bbxml4.xml",
             r"C:\code\shoppersherpa\bestbuyxml\bbxml5.xml",
             r"C:\code\shoppersherpa\bestbuyxml\bbxml6.xml")

# 0 for string, 1 for int, 2 for float, 3 for bool
prod_fields = {
               'productId': 1, 
               'name': 0, 
               'upc': 1, 
               'class': 0, 
               'subclass': 0, 
               'manufacturer': 0, 
               'modelNumber': 0, 
               'width': 0, 
               'longDescription': 0, 
               'warrantyLabor': 0, 
               'warrantyParts': 0,
               'dynamicContrastRatio': 0,
               'maximumResolutionHorizontalPx': 1,
               'maximumResolutionVerticalPx': 1,
               'screenSizeIn': 2,
               'screenSizeClassIn': 1,
               'tvType': 0,
               'verticalResolution': 0} 
offer_fields = {'sku': 1, 'new': 3, 'salesRankLongTerm': 1, 'url': 0}
price_hist_fields = {'regularPrice': 2, 'salePrice': 2, 'onSale': 3, 'shippingCost': 2, 'priceUpdateDate': 0}
review_fields = {'customerReviewAverage': 2, 'customerReviewCount': 1}

field_dicts = (prod_fields, offer_fields, price_hist_fields, review_fields)
def main():
    products_col.remove()
    id = 0

    for xml_filename in filenames:
        xml_file = open(xml_filename)
        xml_str = xml_file.read()
        id = upload_xml(xml_str, id)
      

    count = products_col.count()

def upload_xml(xml, id):
    doc = parseString(xml)
    products = doc.getElementsByTagName("product")

    for prod in products:
        product_object = { '_id': id, 'provider_id': 1, 'offers': [ {'price_history': [ { }] } ], 'reviews': [ { }] }
        
        for node in prod.childNodes:
            if node.nodeType == node.ELEMENT_NODE and node.firstChild != None and node.firstChild.nodeType == node.TEXT_NODE:
                nodeVal = None
                for dict in field_dicts:
                    if node.nodeName in dict.keys():
                        nodeVal = parse_value(node.firstChild.nodeValue, dict[node.nodeName])
                        setPropInProduct(product_object, node.nodeName, nodeVal, dict)
                        break

        products_col.insert(product_object)
        products_col.save(product_object)
        id = id + 1
    return id



def setPropInProduct(product_object, node_name, value, dict):
    if dict is prod_fields:
        product_object[node_name] = value
    elif dict is offer_fields:
        product_object['offers'][0][node_name] = value
    elif dict is price_hist_fields:
        product_object['offers'][0]['price_history'][0][node_name] = value
    elif dict is review_fields:
        product_object['reviews'][0][node_name] = value
    else:
        assert False

def parse_value(val, type):
    if type == 0:
        return val
    elif type == 1:
        return int(val)
    elif type == 2:
        return float(val)
    elif type == 3:
        return (val == 'true')

if __name__=="__main__":
   main()