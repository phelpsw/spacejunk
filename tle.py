#!/usr/bin/env python

import urllib
import urllib2
import cookielib
import json
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
import math
import sys

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


(options, args) = parser.parse_args()

password = ""
if options.password == "":
    import getpass
    password = getpass.getpass()
else:
    password = options.password

cookieJar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
login_uri = 'https://www.space-track.org/ajaxauth/login'
values = {'identity' : options.username,
          'password' : password}
data = urllib.urlencode(values)
opener.open(login_uri, data)

# TODO: check if we successfully logged in

tle_uri = "https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/"+str(options.norad_id)+"/orderby/ORDINAL%20asc/limit/1/metadata/false"
#tle_uri = "https://www.space-track.org/basicspacedata/query/class/tle/NORAD_CAT_ID/"+str(options.norad_id)+"/limit/1/metadata/false"
resp = opener.open(tle_uri)
tle = json.loads(resp.read())[0]

# TODO: Check that we successfully downloaded the tle

#target = ephem.readtle(str(tle['TLE_LINE0']), str(tle['TLE_LINE1']), str(tle['TLE_LINE2']))
#print target

target = twoline2rv(str(tle['TLE_LINE1']), str(tle['TLE_LINE2']), wgs72)

t_zero = datetime.fromtimestamp(int(options.t_zero))
t_minus = timedelta(seconds=int(options.before))
t_plus = timedelta(seconds=int(options.after))

filename = str(options.norad_id) + "_" + t_zero.strftime("%Y_%m_%d_%H_%M_%S.txt")
if options.output:
    filename = options.output
f = open(filename, 'w')

f.write("# Generated at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
f.write("# NORAD ID: " + options.norad_id + "\n")
f.write("# " + str(tle['TLE_LINE1']) + "\n")
f.write("# " + str(tle['TLE_LINE2']) + "\n")
f.write("# t-zero:\n")
f.write("%f\n\n" % float(options.t_zero))

