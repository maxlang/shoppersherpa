from parsing import Product
from numpy import NaN, median,std,isnan,array,equal

data = {}
attrs = []

for p in Product.objects.only('normalized'):
    attrs.append(p.normalized)

print 'loaded in products'



from matplotlib import pyplot, cm, colors

def genplots(save=False, folder="images", **kwargs):
    if save:
        import os
        folder = os.path.join(os.getcwd(), folder)
        if not os.path.exists(folder):
            os.mkdir(folder)

    for key in ('price', 'size_class', 'ratings_avg', 'brand', 'refresh', 'is_3d', 'tv_type', 'resolution'):
        data[key] = []
        for a in attrs:
            try:
                if key in ('price', 'size_class', 'ratings_avg', 'refresh'):
                    if a[key]:
                        precision = 0
                        accuracy = 1
                        if key in ['price', 'refresh']:
                            precision = -1
                        elif key in ['size_class']:
                            accuracy = 2
                        elif key in ['ratings_avg']:
                            precision = 0
                        data[key].append(round(float(a[key]) / accuracy, precision) * accuracy)
                    else:
                        data[key].append(NaN)
                else:
                    if hasattr(a[key], 'strip'):
                        data[key].append(a[key].strip(u'\x99'))
                    else:
                        data[key].append(a[key])
            except KeyError:
                print (u"Couldn't find key: %s for product with attributes: %s" % (key, a))
        unique = sorted(list(set(data[key])))
        data[key + "map"] = array([unique.index(item) for item in data[key]])
        data[key] = array(data[key])

        largelims = None
        zoomlims = None

        if 'price' in data and 'size_class' in data and not largelims and not zoomlims:
            xbuf = 5
            ybuf = 100
            largelims = {'xmax':max(data['size_class']) + xbuf,
                         'xmin':min(data['size_class']) - xbuf,
                         'ymax':max(data['price']) + ybuf,
                         'ymin':min(data['price']) - ybuf}

            xmed = median(data['size_class'])
            xsd = std(data['size_class'][:, ~isnan(data['size_class'])])
            ymed = median(data['price'])
            ysd = std(data['price'][:, ~isnan(data['price'])])
            zoomlims = {'xmax':xmed + xsd / 2,
                        'xmin':xmed - xsd / 2,
                        'ymax':ymed + ysd / 2,
                        'ymin':ymed - ysd / 2}


        if key not in ('price', 'size_class') and largelims and zoomlims:
            largename = key + "large"
            pyplot.figure(largename, figsize=(20, 15))
            pyplot.xlim(xmax=largelims['xmax'], xmin=largelims['xmin'])
            pyplot.ylim(ymax=largelims['ymax'], ymin=largelims['ymin'])
            pyplot.title(largename)
            zoomname = key + "zoom"
            pyplot.figure(zoomname, figsize=(20, 15))
            pyplot.xlim(xmax=zoomlims['xmax'], xmin=zoomlims['xmin'])
            pyplot.ylim(ymax=zoomlims['ymax'], ymin=zoomlims['ymin'])
            pyplot.title(zoomname)

            #TODO: better nan handling
            if key in ['price', 'size_class', 'ratings_avg', 'refresh']:
                values = data[key][:, ~isnan(data[key])]
                prices = data['price'][:, ~isnan(data[key])]
                sizes = data['size_class'][:, ~isnan(data[key])]
            else:
                values = data[key][:, ~equal(data[key], None)]
                prices = data['price'][:, ~equal(data[key], None)]
                sizes = data['size_class'][:, ~equal(data[key], None)]
            for value in set(values):
                if len(values[:, equal(values, value)]) >2:
                    print "graphing with key: %s and value %s" % (key, unicode(value))
                    pyplot.figure(largename)
                    color = (float(unique.index(value))) / (float(len(unique)))
                    edgecolor = color#max(0,color-.2)
                    if kwargs['cmap']:
                        edgecolor = kwargs['cmap'](int(round(float(kwargs['cmap'].N) * float(edgecolor))))
                        color = kwargs['cmap'](int(round(float(kwargs['cmap'].N) * color)))
                    else:
                        edgecolor = str(edgecolor)
                        color = str(color)

                    cursizes = sizes[:, values == value]
                    curprices = prices[:, values == value]
                    rectlarge = pyplot.Rectangle((min(cursizes) - 1, min(curprices) - 10),
                                            max(cursizes) - min(cursizes) + 2,
                                            max(curprices) - min(curprices) + 20,
                                            edgecolor=edgecolor,
                                            linewidth=10,
                                            facecolor=color,
                                            alpha=.1)
                    pyplot.scatter(cursizes, curprices, c=color, label=unicode(value), norm=colors.NoNorm(), **kwargs)#c=data[key+'map'],,cmap=cm.gray)
                    pyplot.gca().add_patch(rectlarge)
                    pyplot.gca().text(max(largelims['xmin'] + 1, min(cursizes) + 2),
                                       min(largelims['ymax'] - 100,max(curprices) - 300),unicode(value))
                    pyplot.figure(zoomname)
                    rectzoom = pyplot.Rectangle((min(cursizes) - 1,min(curprices) - 10),
                        max(cursizes)-min(cursizes)+2,
                        max(curprices)-min(curprices)+20,
                        edgecolor=edgecolor,
                        linewidth=10,
                        facecolor=color,
                        alpha=.1)
                    pyplot.scatter(cursizes,curprices,c=color,label=unicode(value),**kwargs)#,c=data[key+'map'],cmap=cm.gray)
                    pyplot.gca().add_patch(rectzoom)
                    pyplot.gca().text(min(cursizes)+1,min(zoomlims['ymax']-100,max(curprices)),unicode(value))
                else:
                    print "rejecting key: %s and value %s" % (key,unicode(value))

            pyplot.figure(largename)
            pyplot.legend()
            if save:
                pyplot.savefig("%s/%s.png" % (folder,largename))


            pyplot.figure(zoomname)
            pyplot.legend()

            if save:
                pyplot.savefig("%s/%s.png" % (folder, zoomname))
genplots(save=False, folder="squares", s=400, cmap=cm.jet)
pyplot.show()
'''

sz = data['size']
pr = data['price']

from numpy import *

asz = array(sz)
apr = array(pr)

rasz = around(asz)
rapr = around(apr)

heatmap = zeros((max(rapr),max(rasz)))

for i in range(len(rapr)):
    heatmap[rapr[i]-1,rasz[i]-1]+=1

#from here - we'll probably want to write our own
#http://mail.scipy.org/pipermail/scipy-user/2006-June/008366.html
def makeGaussian(size, fwhm = 3):
    """ Make a square gaussian kernel.

    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    """

    x = arange(0, size, 1, float32)
    y = x[:,newaxis]
    x0 = y0 = size // 2
    return exp(-4*log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)
#

from matplotlib import pyplot,cm
def tryGraph(ratio=100,bins=20,cmap=cm.Greys,xlim=(40,70),ylim=(500,2000),interpolation='nearest'):
    heatmap, xedges, yedges = histogram2d(rasz,rapr, bins=bins)
    extent = [xedges[0], xedges[-1], yedges[0]/ratio, yedges[-1]/ratio]
    print extent
    shape(heatmap)
    pyplot.figure(1)
    pyplot.imshow(rot90(log(heatmap+1)),extent=extent,cmap=cmap,aspect="equal",interpolation=interpolation)
    pyplot.ylim(ylim[0]/ratio,ylim[1]/ratio)
    pyplot.xlim(xlim)
    pyplot.colorbar()
    locations,labels = pyplot.yticks()
    pyplot.yticks(locations,locations*ratio)
    pyplot.figure(2)
    pyplot.imshow(rot90(heatmap),extent=extent,cmap=cmap,aspect="equal",interpolation=interpolation)
    pyplot.ylim(ylim[0]/ratio,ylim[1]/ratio)
    pyplot.xlim(xlim)
    pyplot.colorbar()
    locations,labels = pyplot.yticks()
    pyplot.yticks(locations,locations*ratio)
    pyplot.show()
#import matplotlib.pyplot as plt
#plt.plot(sz, pr, 'ro')
#plt.show()

'''