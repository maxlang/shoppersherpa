from xml.dom.minidom import parseString
from mongomodels import *

filenames = (r"C:\github\shoppersherpa\xml\bbxml1.xml",
             r"C:\github\shoppersherpa\xml\bbxml2.xml",
             r"C:\github\shoppersherpa\xml\bbxml3.xml",
             r"C:\github\shoppersherpa\xml\bbxml4.xml",
             r"C:\github\shoppersherpa\xml\bbxml5.xml",
             r"C:\github\shoppersherpa\xml\bbxml6.xml")

def main():
    Product.objects.delete()
    id = 0

    for xml_filename in filenames:
        xml_file = open(xml_filename)
        xml_str = xml_file.read()
        id = upload_xml(xml_str, id)

def upload_xml(xml, id):
    doc = parseString(xml)
    products = doc.getElementsByTagName("product")

    for prod in products:
        mongoProduct = Product()
        
        for node in prod.childNodes:
            if node.nodeType == node.ELEMENT_NODE and node.firstChild != None and node.firstChild.nodeType == node.TEXT_NODE:
                nodeVal = parse_value(node.firstChild.nodeValue)
                mongoProduct.attr[node.nodeName]= nodeVal
        mongoProduct.save()

def parse_value(val):
    try:
        return int(val)
    except:
        pass
    try:
        return float(val)
    except:
        pass
    if val in ['true', 'True', 'TRUE']:
        return True
    if val in ['false', 'False', 'FALSE']:
        return False
    return val

if __name__=="__main__":
   main()
