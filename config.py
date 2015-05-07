# -*- coding: utf-8 -*-

from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap

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

# LIGHT_BLUE = (166,206,227)
# DARK_BLUE = 31,120,180
# GREEN = 178,223,138

LIGHT_BLUE = '#a6cee3'
DARK_BLUE = '#1f78b4'
GREEN = '#b2df8a'

COLORS = ['#e41a1c', '#377eb8', '#4daf4a']

TRANSPARENT_WHITE = colors.ColorConverter().to_rgba('white', alpha=0)

COLOR_MAPS = [LinearSegmentedColormap.from_list('', [TRANSPARENT_WHITE, color]) for color in COLORS]
