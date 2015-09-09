import numpy as np

from enum import Enum
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from apis import twitter_api


class BoundingBox(object):
    pass


class Place(object):
    def __init__(self, twitter_place_id):
        response = twitter_api.api.geo_id(twitter_place_id)
        self.centroid_lat = response.centroid[0]
        self.centroid_lon = response.centroid[1]


EUROPE_RESTRICTED = BoundingBox()
EUROPE_RESTRICTED.north_east_lat = 72  # 62
EUROPE_RESTRICTED.north_east_lon = 30  # 20
EUROPE_RESTRICTED.south_west_lat = 35
EUROPE_RESTRICTED.south_west_lon = -12

EUROPE = BoundingBox()
EUROPE.north_east_lat = 81.008797
EUROPE.north_east_lon = 39.869301
EUROPE.south_west_lat = 27.636311
EUROPE.south_west_lon = -31.266001

ZURICH_EXTENDED = BoundingBox()
ZURICH_EXTENDED.north_east_lat = 47.434680
ZURICH_EXTENDED.north_east_lon = 8.625370
ZURICH_EXTENDED.south_west_lat = 47.320230
ZURICH_EXTENDED.south_west_lon = 8.448060

LONDON_CITY = Place(twitter_api.PLACE_ID_LONDON_CITY)


class MapResolution(Enum):
    INTERMEDIATE = 1
    FULL = 2


class Map(object):
    def __init__(self, bounding_box, map_resolution=MapResolution.INTERMEDIATE):
        basemap = Basemap(resolution=map_resolution.name[0].lower(),
                          urcrnrlat=bounding_box.north_east_lat,
                          urcrnrlon=bounding_box.north_east_lon,
                          llcrnrlat=bounding_box.south_west_lat,
                          llcrnrlon=bounding_box.south_west_lon)
        basemap.drawcountries(linewidth=0.25)
        basemap.drawcoastlines(linewidth=0.25)
        basemap.arcgisimage(xpixels=6000)
        # basemap.bluemarble()
        # map.shadedrelief()
        # basemap.fillcontinents(color='peru', lake_color='yellow')
        # basemap.drawrivers(color='blue', linewidth=0.1)
        self._basemap = basemap
        self._bounding_box = bounding_box

    def draw_points(self, points):
        for point in points:
            mapped_lon, mapped_lat = self._basemap(point.lon, point.lat)
            map.plot(mapped_lon, mapped_lat, 'ro', 15, alpha=0.5)

    def draw_densities(self, points, n_bins, color_map='Blues'):
        lons = np.array([p.lon for p in points], dtype=float)
        lats = np.array([p.lat for p in points], dtype=float)

        density_lon_range = (self._bounding_box.south_west_lon, self._bounding_box.north_east_lon)
        density_lat_range = (self._bounding_box.south_west_lat, self._bounding_box.north_east_lat)
        density_range = (density_lon_range, density_lat_range )
        density, bin_edges_x, bin_edges_y = np.histogram2d(lons, lats, bins=n_bins, range=density_range)

        log_density = np.log10(density)
        log_density[log_density < 0] = 0

        bin_lons, bin_lats = np.meshgrid(bin_edges_x, bin_edges_y)
        mapped_bin_lons, mapped_bin_lats = self._basemap(bin_lons, bin_lats)

        plt.pcolormesh(mapped_bin_lons, mapped_bin_lats, log_density.transpose(), cmap=color_map, label='toco')

    def show(self):
        plt.show()

    def save(self, path, format='png'):
        plt.savefig(path, format=format, dpi=300)


class Point(object):
    pass


if __name__ == '__main__':
    map = Map(ZURICH_EXTENDED)
    map.show()