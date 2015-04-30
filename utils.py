import logging
from time import time
from mpl_toolkits.basemap import Basemap
from apis import flickr_api


def assess(query, per_page):

    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    total = flickr_api.count_photos(query)

    print '\nQuery: %s' % query
    print 'Params: %s \n' % flickr_api._get_params(query)
    print 'Results per page: %s' % per_page
    print 'Total: %s' % total

    start = time()
    points = flickr_api.get_points(query, per_page=per_page)
    end = time()
    seconds = end - start

    print 'Total (counted): %s' % len(points)
    print 'time: %.2f seconds' % seconds






