import urllib
from xml.dom.minidom import parse, parseString

url = "http://api.remix.bestbuy.com/v1/products(categoryPath.name=TVs)?pageSize=75&page=%i&apiKey=ucyz9yc539n69pd6grutj9yx"
outfilename = "c:\\code\\shoppersherpa\\bestbuyxml\\bbxml%i.xml"


# Get a file-like object for the Python Web site's home page.
f = urllib.urlopen(url % (1))
# Read from the object, storing the page's contents in 's'.
s = f.read()
f.close()

doc = parseString(s)

products_el = doc.getElementsByTagName("products")
num_pages = int(products_el[0].getAttribute("totalPages"))

outf = open(outfilename % (1), 'w')
outf.write(s)
outf.close()

print num_pages

for pg in range(2, num_pages + 1):
    f = urllib.urlopen(url % (pg))
    s = f.read()
    f.close()

    outf = open(outfilename % (pg), 'w')
    outf.write(s)
    outf.close() 


#print s
