# Mapping Engine

## Generate GeoJSON base map

Based on the sample here http://bost.ocks.org/mike/map/

And this really excellent site: http://www.naturalearthdata.com/downloads/50m-physical-vectors/

This only needs to occur once to render the map against which all else will be rendered.

sudo apt-get install gdal-bin nodejs npm nodejs-legacy
sudo npm install -g topojson

http://www.naturalearthdata.com/downloads/50m-physical-vectors/
wget http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/physical/ne_50m_coastline.zip

git clone https://github.com/mbostock/world-atlas.git
cd world-atlas
npm install
make topo/world-50m.json

Alternative mapping library: http://matplotlib.org/basemap/users/examples.html


# Association Server

Runs periodically, gathers list of all norad ids.  For each norad id, looks up associated objects.  Updates the associated objects list for a user (with the exception of listed objects)


# TLE Update server

## TLE Update Thread

Runs once every day.

Responsible for building a list of norad ids to update.  It then makes the necessary requests to space-track.org and stores the resulting TLE in a map.  Because the entire space-track catalog (50k sats * 200B per listing) can fit into about 10MB this doesn't seem unreasonable.


## TLE Propagation Thread
For each norad id, update the current position and update mongodb.

## Setup
sudo apt-get install mongod
sudo pip install pymongo
sudo pip install pyephem

mongo
use satdb
user = {name : "phelps", objects : [1, 2, 3]}
db.users.insert(user)
user = {name : "bob", objects : [2, 3, 4]}
db.users.insert(user)

sat = {norad: 1, latitude: 10.0, longitude: -10.0}
db.satellites.insert(sat)
sat = {norad: 2, latitude: 20.0, longitude: -20.0}
db.satellites.insert(sat)
sat = {norad: 3, latitude: 30.0, longitude: -30.0}
db.satellites.insert(sat)
sat = {norad: 4, latitude: 40.0, longitude: -40.0}
db.satellites.insert(sat)

db.users.distinct('objects')

# Mapping server

Looks up satellites associated with given userid.  Takes the positions of each satellite and returns last calculated location.


