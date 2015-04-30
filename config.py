# -*- coding: utf-8 -*-

from geo import BoundingBox

START_YEAR = 2000
END_YEAR = 2015

EUROPE_RESTRICTED = BoundingBox()
EUROPE_RESTRICTED.north_east_lat =  72 # 62
EUROPE_RESTRICTED.north_east_lon = 30 #20
EUROPE_RESTRICTED.south_west_lat = 35
EUROPE_RESTRICTED.south_west_lon = -12

EUROPE = BoundingBox()
EUROPE.north_east_lat = 81.008797
EUROPE.orth_east_lon = 39.869301
EUROPE.south_west_lat = 27.636311
EUROPE.south_west_lon = -31.266001


FLOODING_TAGS = dict()
FLOODING_TAGS['de'] = 'hochwasser, überschwemmung, überflutung, flut'
