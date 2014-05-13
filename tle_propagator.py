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
    db.satellites.update({'norad': sat['norad']},
	    {'$set' : {'lat' : target.sublat * rad_to_deg,
		       'lon' : target.sublong * rad_to_deg}})
runtime = datetime.now() - start
print "tle_propagator.py %d satellites, runtime: %s, %s/sat" % \
	(sats.count(), runtime, runtime / sats.count())

