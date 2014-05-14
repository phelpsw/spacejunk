#!/usr/bin/env python

from pymongo import MongoClient
import urllib
import urllib2
import cookielib
import json
import sys



client = MongoClient('localhost', 27017)
db = client.satdb

norad_ids = db.users.distinct('objects')

# TODO: there is probably a better way to do this
from config import username, password

cookieJar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
login_uri = 'https://www.space-track.org/ajaxauth/login'
values = {'identity' : username,
          'password' : password}
data = urllib.urlencode(values)
opener.open(login_uri, data)

# TODO: check if we successfully logged in

for norad_id in norad_ids:
    tle_uri = "https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/"+str(int(norad_id))+"/orderby/ORDINAL%20asc/limit/1/metadata/false"
    try:
	resp = opener.open(tle_uri)
	tle = json.loads(resp.read())[0]
	print tle

	# TODO: check if object has decayed!

	db.satellites.update({'norad': int(norad_id)},
		{'norad': int(norad_id),
		 'name': str(tle['OBJECT_NAME']),
		 'tle1': str(tle['TLE_LINE1']),
		 'tle2': str(tle['TLE_LINE2']),
		 'status' : 'alive'},
		upsert=True)
    except IndexError:
	# TODO: consider status == invalid
	db.satellites.update({'norad': int(norad_id)},
		{'norad': int(norad_id), 'status': 'dead'},
		upsert=True)
    except:
	print "Unexpected error:", sys.exc_info()[0]
	pass

