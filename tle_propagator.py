#!/usr/bin/env python

from pymongo import MongoClient
import ephem
from datetime import datetime
from math import pi

start = datetime.now()
client = MongoClient('localhost', 27017)
db = client.satdb

sats = db.satellites.find({'status' : 'alive'})
rad_to_deg = 180.0 / pi
for sat in sats:
    target = ephem.readtle(str(sat['name']), str(sat['tle1']), str(sat['tle2']))
    target.compute(datetime.utcnow())

    # Quick and dirty way to calc apogee and perigee from Ted Molczan
    # http://www.satobs.org/seesat/Dec-2002/0197.html
    a = (8681663.653 / target._n) ** (2.0/3.0)
    perigee = a * (1 - target._e) - 6371.0
    apogee = a * (1 + target._e) - 6371.0

    db.satellites.update({'norad': sat['norad']},
	    {'$set' : {'lat' : target.sublat * rad_to_deg,
		       'lon' : target.sublong * rad_to_deg,
		       'perigee' : perigee,
		       'apogee' : apogee}})
runtime = datetime.now() - start
print "tle_propagator.py %d satellites, runtime: %s, %s/sat" % \
	(sats.count(), runtime, runtime / sats.count())

