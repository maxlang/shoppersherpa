from parsing import ParsedProduct

pr = []
sz = []

for p in ParsedProduct.objects:
    try:
        sz.append(p.attr['screenSizeIn']);
        pr.append(p.attr['regularPrice']);
        continue
    except KeyError:
        pass
    try:
        sz.append(p.attr['screenSizeClassIn']);
        pr.append(p.attr['regularPrice']);
    except KeyError:
        print (u"Couldn't find any key for product with attributes:",
               p.parsedAttr)

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
