# -*- coding: utf-8 -*-

# todo: highly refactor!
import os
from os.path import join

from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
from os import path

ROOT_DIR = '/home/dominic/projects/social-media-mining'
TWITTER_PLOT_DIR = join(ROOT_DIR, 'plots', 'twitter')
if not path.exists(TWITTER_PLOT_DIR):
    os.makedirs(TWITTER_PLOT_DIR)

# LIGHT_BLUE = (166,206,227)
# DARK_BLUE = 31,120,180
# GREEN = 178,223,138

LIGHT_BLUE = '#a6cee3'
DARK_BLUE = '#1f78b4'
GREEN = '#b2df8a'

COLORS = ['#e41a1c', '#377eb8', '#4daf4a']

TRANSPARENT_WHITE = colors.ColorConverter().to_rgba('white', alpha=0)

COLOR_MAPS = [LinearSegmentedColormap.from_list('', [TRANSPARENT_WHITE, color]) for color in COLORS]
