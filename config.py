# -*- coding: utf-8 -*-

from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap

from apis.flickr_api import FlickrQuery
from geo import BoundingBox

# LIGHT_BLUE = (166,206,227)
# DARK_BLUE = 31,120,180
# GREEN = 178,223,138

LIGHT_BLUE = '#a6cee3'
DARK_BLUE = '#1f78b4'
GREEN = '#b2df8a'

COLORS = ['#e41a1c', '#377eb8', '#4daf4a']

TRANSPARENT_WHITE = colors.ColorConverter().to_rgba('white', alpha=0)

COLOR_MAPS = [LinearSegmentedColormap.from_list('', [TRANSPARENT_WHITE, color]) for color in COLORS]
