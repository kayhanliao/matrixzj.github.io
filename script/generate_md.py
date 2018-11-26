#! /usr/bin/python

from sys import argv
from os import listdir
import os
from os.path import isfile, join

script, filepath = argv

rateDict = {"2018-11": '6.95', "2018-10": '6.87', "2018-09": '6.95',
    "2018-08": '6.87',"2018-07": '6.67',"2018-06": '6.47',"2018-05": '6.42',
    "2018-04": '6.34',"2018-03": '6.28',"2018-02": '6.29',"2018-01": '6.29', 
    "2017-12": '',"2017-11": '',"2017-10": '',"2017-09": '',
    "2017-08": '',"2017-07": '',"2017-06": '8.85',"2017-05": '',
    "2017-04": '',"2017-03": '',"2017-02": '',"2017-01": '',
    "2016-12": '',"2016-11": '',"2016-10": '',"2016-09": '',
    "2016-08": '',"2016-07": '',"2016-06": '',"2016-05": '',
    "2016-04": '',"2016-03": '',"2016-02": '',"2016-01": '',
    "2015-12": '',"2015-11": '',"2015-10": '',"2015-09": '',
    "2015-08": '',"2015-07": '',"2015-06": '',"2015-05": '',
    "2015-04": '',"2015-03": '',"2015-02": '',"2015-01": '',
    "2014-12": '',"2014-11": '',"2014-10": '',"2014-09": '',
    "2014-08": '',"2014-07": '',"2014-06": '',"2014-05": '',
    "2014-04": '',"2014-03": '',"2014-02": '',"2014-01": '',
    "2013-12": '',"2013-11": '',"2013-10": '',"2013-09": '',
    "2013-08": '',"2013-07": '',"2013-06": '',"2013-05": '',
    "2013-04": '',"2013-03": '',"2013-02": '',"2013-01": '',
    "2012-12": '',"2012-11": '',"2012-10": '',"2012-09": '',
    "2012-08": '',"2012-07": '',"2012-06": '',"2012-05": '',
    "2012-04": '',"2012-03": '',"2012-02": '',"2012-01": '',}

lines = tuple(open(filepath, 'r'))

# get Name
name = lines[0].split("'")[1]

# get cName
cname = lines[1].split("'")[1]

# get keycaptype
keycapstype = lines[2].split("'")[1]

# get time
time = lines[5].split("'")[1]

# get rate
if rateDict[time]:
    rate = float(rateDict[time])
else:
    rate = ''

# get designer
designer = lines[3].split("'")[1]

# get profile
profile = lines[4].split("'")[1]

# get colorcodes
colorcodes = lines[6].split("'")[1]

# get plateform
platform = lines[7].split("'")[1]

# get link
link = lines[8].split("'")[1]

# generate navOrder
keycapPath = '/home/juzou/documents/matrixzj.github.io/docs/%s-keycaps/' % keycapstype.lower()
navOrder = ( len([eachfile for eachfile in os.listdir(keycapPath) if os.path.isfile(os.path.join(keycapPath, eachfile))]) - 1) * 5 + 10000

# key: name, usd, rmb, proxyprice, quantity
priceDict = {}
sn = 1
for line in lines[9:]:
    lengthLine = len(line.split("|"))
    if lengthLine == 6:
	hasQuantity = True
    else:
	hasQuantity = False

    kitName = line.split("|")[0]

    kitUSD = line.split("|")[1]
    
    if len(kitUSD) < 1:
        kitUSD = 'unknown'
    else:
        kitUSD = float(kitUSD)

    kitRMB = line.split("|")[2]
    if len(kitRMB) < 1 and isinstance(kitUSD, float):
        kitRMB = float(kitUSD) * rate
    elif len(kitRMB) > 1:
        kitRMB = float(kitRMB)
    else:
	kitRMB = 'unknown'

    kitPlatformPrice = line.split("|")[3]
    if platform:
        if len(kitPlatformPrice) < 1:
            kitPlatformPrice = 'unknown'
        else:
            float(kitPlatformPrice)

    if hasQuantity:
        kitQuantity = line.split("|")[4]
	if len(kitQuantity) < 1:
	    kitQuantity = 'unknown'
	else:
	    int(kitQuantity)

    if hasQuantity:
	priceDict[sn] = [kitName, kitUSD, kitRMB, kitPlatformPrice, kitQuantity]
    else:
	priceDict[sn] = [kitName, kitUSD, kitRMB, kitPlatformPrice]
    sn += 1

print "---\ntitle: %s %s\nlayout: default\nicon: fa-keyboard-o\nparent: %s Keycaps\nnav_order: %d\n---\n\n# %s %s\n\nref link: [%s %s GB Link](%s)\n\n* [Price](#price)\n* [Kits](#kits)\n* [Info](#info)\n* [Pictures](#pictures)\n\n\n## Price  " % (name, cname, keycapstype, navOrder, name, cname, name, platform, link)

if rate:
    print 'NOTE: USD to RMB exchange rate is %.2f' % rate

# generate price table
if hasQuantity: 	
    print """
| Name          | Price(USD)    |  Price(RMB) |  Price(%s) | Quantity |
| ------------- | ------------- |  ---------- |  --------- | -------- |""" % platform
else:
    print """
| Name          | Price(USD)    |  Price(RMB) |  Price(%s) |
| ------------- | ------------- |  ---------- |  --------- |""" % platform

for i in priceDict:
    # check USD
    if isinstance(priceDict[i][1], float):
        printPriceFormat = "|[%s](#%s)|%.2f|"
        printKitFormat = "**Price(USD):** %.2f    "
    else:
        printPriceFormat = "|[%s](#%s)|%s|"
        printKitFormat = "**Price(USD):** %s    "

    # check RMB
    if isinstance(priceDict[i][2], float):
        printPriceFormat = printPriceFormat + "%.2f|"
        printKitFormat = printKitFormat + "**Price(RMB):** %.2f    "
    else:
        printPriceFormat = printPriceFormat + "%s|"
        printKitFormat = printKitFormat + "**Price(RMB):** %s    "

    # check PlateformPrice
    if platform: 
        if isinstance(priceDict[i][3], float):
            printPriceFormat = printPriceFormat + "%.2f|"
            printKitFormat = printKitFormat + "**Price(%s):** %.2f    "
        else:
            printPriceFormat = printPriceFormat + "%s|"
            printKitFormat = printKitFormat + "**Price(%s):** %s    "

    # check Quantity
    if hasQuantity:
        if isinstance(priceDict[i][4], int):
            printPriceFormat = printPriceFormat + "%d|"
            printKitFormat = printKitFormat + "**Quantity:** %d  "
        else:
            printPriceFormat = printPriceFormat + "%s|"
            printKitFormat = printKitFormat + "**Quantity:** %s  "

    if hasQuantity:
        print printPriceFormat % (priceDict[i][0], priceDict[i][0].lower().replace(" ",""), priceDict[i][1], priceDict[i][2], priceDict[i][3], priceDict[i][4])
    else:
        print printPriceFormat % (priceDict[i][0], priceDict[i][0].lower().replace(" ",""), priceDict[i][1], priceDict[i][2], priceDict[i][3])

priceRelFilePath = 'assets/images/%s-keycaps/%s/price.jpg' % ( keycapstype, name.lower().replace(" ","") )
priceAbsFilePath = os.path.join('/home/juzou', priceRelFilePath)
if os.path.isfile(priceAbsFilePath):
    print ''
    print '<img src="{{ \'assets/images/%s-keycaps/%s/price.jpg\' | relative_url }}" alt="price" class="image featured">' % (keycapstype, name.lower().replace(" ",""))

print ''
print ''

print '## Kits'
for i in priceDict:
    print '### %s' % priceDict[i][0]
    if hasQuantity:
        print printKitFormat % (priceDict[i][1], priceDict[i][2], platform, priceDict[i][3], priceDict[i][4])
    else:
	print printKitFormat % (priceDict[i][1], priceDict[i][2], platform, priceDict[i][3])

    imagePrintFormat = "<img src=\"{{ 'assets/images/%s-keycaps/%s/kits_pics/%s.jpg' | relative_url }}\" alt=\"%s\" class=\"image featured\">"
    print imagePrintFormat % (keycapstype.lower(), name.lower().replace(" ",""), priceDict[i][0].lower().replace(" ","-"), priceDict[i][0])
    print ''

print ''
    
# 
# generate info part
#
print """## Info
* Designer: %s
* Profile: %s %s""" % (designer, keycapstype, profile)
print "* GB Time: %s" % time
if keycapstype == "SA" and colorcodes != '' :
    print "* Color Codes: %s  " % (colorcodes)
    for color in colorcodes.split('/'):
        print '<img src="{{ \'assets/images/sa-keycaps/SP_ColorCodes/abs/SP_Abs_ColorCodes_%s.png\' | relative_url }}" alt="color%s" height="150" width="340">' % (color, color)
elif keycapstype == "SA" and colorcodes == '' :
    print "* Color Codes: unknown  "
elif keycapstype == "GMK" :
    print "* ColorCodes: as shown in kits pictures"
print ''
print ''

#
# generate picture part
#
picPath = '/home/juzou/documents/matrixzj.github.io/assets/images/%s-keycaps/%s/rendering_pics/' % (keycapstype.lower(), name.lower().replace(" ",""))
if os.path.isdir(picPath):
    print '## Pictures'
    pictures = [f for f in listdir(picPath)]
    for pic in pictures:
       print '<img src="{{ \'assets/images/%s-keycaps/%s/rendering_pics/%s\' | relative_url }}" alt="%s" class="image featured">' % ( keycapstype.lower(), name.lower().replace(" ",""), pic, pic.replace(".jpg","") )


# generate index
print "* [%s %s](docs/%s-keycaps/%s/)" % (name, cname, keycapstype.lower(), name.replace(' ','-'))

