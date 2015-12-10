# -*- coding: utf-8 -*-

# todo: highly refactor!

import os
from os import path

from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
try:
    from main.local_config import ROOT_DIR
except:
    raise RuntimeError('No ROOT_DIR defined in module local_config')

DATA_DIR = path.join(ROOT_DIR, 'data')
PLOTS_DIR = path.join(ROOT_DIR, 'plots')
MISC_PLOTS_DIR = path.join(PLOTS_DIR, 'misc')
DOCS_IMG_DIR = path.join(ROOT_DIR, 'docs', 'source', 'img')

for dir_path in (MISC_PLOTS_DIR, DOCS_IMG_DIR):
    os.makedirs(dir_path, exist_ok=True)


# LIGHT_BLUE = (166,206,227)
# DARK_BLUE = 31,120,180
# GREEN = 178,223,138

LIGHT_BLUE = '#a6cee3'
DARK_BLUE = '#1f78b4'
GREEN = '#b2df8a'

COLORS = ['#e41a1c', '#377eb8', '#4daf4a']

TRANSPARENT_WHITE = colors.ColorConverter().to_rgba('white', alpha=0)

COLOR_MAPS = [LinearSegmentedColormap.from_list('', [TRANSPARENT_WHITE, color]) for color in COLORS]
