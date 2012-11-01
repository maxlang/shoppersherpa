from parsing import ParsedProduct

price = []
size = []

for p in ParsedProduct.objects:
    try:
        size.append(p.attr['screenSizeIn']);
        price.append(p.attr['regularPrice']);
    except KeyError:
        pass
    try:
        size.append(p.attr['screenSizeClassIn']);
        price.append(p.attr['regularPrice']);
    except KeyError:
        print (u"Couldn't find any key for product with attributes:", 
               p.parsedAttr)

import matplotlib.pyplot as plt
plt.plot(size, price, 'ro')
plt.show()
