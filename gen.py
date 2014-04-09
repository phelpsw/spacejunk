#!/usr/bin/env python

import json
import ephem

json_data=open('db.json')
db = json.load(json_data)

print db['pw']
# https://www.space-track.org/basicspacedata/query/class/tle_latest/INTLDES/~~98067/orderby/ORDINAL%20asc/format/html/metadata/false
tle0 = "ISS (ZARYA)"
tle1 = "1 25544U 98067A   14098.69383451  .00017787  00000-0  31206-3 0   379"
tle2 = "2 25544  51.6497  83.9654 0002160   3.2766 159.0920 15.50620611880540"

tle_rec = ephem.readtle(tle0, tle1, tle2)
tle_rec.compute()

print tle_rec.sublong, tle_rec.sublat, tle_rec.elevation

# sudo apt-get install python-matplotlib python-mpltoolkits.basemap

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
#m = Basemap(width=12000000,height=9000000,projection='lcc',
#                        resolution=None,lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
#m = Basemap(projection='hammer',lon_0=180)
#m = Basemap(projection='kav7',lon_0=0,resolution=None)
m = Basemap(projection='eck4',lon_0=0,resolution='c')
m.drawcoastlines()
m.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
m.drawmeridians(np.arange(m.lonmin,m.lonmax+30,60),labels=[0,0,0,1])
# fill continents 'coral' (with zorder=0), color wet areas 'aqua'
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral',lake_color='aqua')

date = datetime.utcnow()
CS = m.nightshade(date)

import math
def dms2deg(v):
    return (ephem.degrees(v) / (2 * math.pi)) * 360.0

names = [tle0]
lats = [dms2deg(tle_rec.sublat)]
lons = [dms2deg(tle_rec.sublong)]
print lats, lons
x, y = m(lons, lats)
print x, y
#m.scatter(x,y,20,marker='o',color='r')

m.plot(x,y,'ro')
# plot the names of those five cities.
for name,xpt,ypt in zip(names,x,y):
    plt.text(xpt+50000,ypt+50000,name)

plt.show()

