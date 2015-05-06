import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap


__author__ = 'dominic'


class BoundingBox(object):
    pass


class Map(object):
    def __init__(self, bounding_box):
        basemap = Basemap(resolution='i',
                          urcrnrlat=bounding_box.north_east_lat,
                          urcrnrlon=bounding_box.north_east_lon,
                          llcrnrlat=bounding_box.south_west_lat,
                          llcrnrlon=bounding_box.south_west_lon)
        basemap.drawcountries(linewidth=0.5)
        basemap.drawcoastlines(linewidth=0.5)
        # map.shadedrelief()
        # map.fillcontinents(color='peru', zorder=0)
        # map.drawrivers(color='blue')
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

        plt.pcolormesh(mapped_bin_lons, mapped_bin_lats, log_density.transpose(), cmap=color_map)
        plt.colorbar(shrink=0.75)

    def show(self):
        plt.show()


class Point(object):
    pass