# -*- coding: utf-8 -*-

from matplotlib import colors

from apis.flickr_api import FlickrQuery, QueryType
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
EUROPE.north_east_lon = 39.869301
EUROPE.south_west_lat = 27.636311
EUROPE.south_west_lon = -31.266001


FLOODING_GERMAN_TAGS_QUERY = FlickrQuery(language='de', query_type=QueryType.TAGS, only_geotagged=True)
FLOODING_ENGLISH_TAGS_QUERY = FlickrQuery(language='en', query_type=QueryType.TAGS, only_geotagged=True)
FLOODING_FRENCH_TAGS_QUERY = FlickrQuery(language='fr', query_type=QueryType.TAGS, only_geotagged=True)


TRANSPARENT_WHITE = colors.ColorConverter().to_rgba('white', alpha=0)
D_REDS = colors.LinearSegmentedColormap.from_list('d_reds', [TRANSPARENT_WHITE, 'red'])