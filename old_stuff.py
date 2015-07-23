

def print_random_links(query):
    params = flickr_api._get_params(query)
    photos = flickr_api._get_photos_from_params(params)

    for _ in range(5):
        url = photos.get_random_link()
        print(url)

def _get_params(query, with_geotags=False):
    """

    :rtype : dict
    """

    if query == FlickrQuery.switzerland:
        params['woe_id'] = WOE_ID_SWITZERLAND

    elif query == FlickrQuery.switzerland_flooding_text:
        params['woe_id'] = WOE_ID_SWITZERLAND
        params['text'] = 'hochwasser'

    elif query == FlickrQuery.switzerland_flooding_tags:
        params['woe_id'] = WOE_ID_SWITZERLAND
        params['tags'] = FLOODING_TAGS_DE

    elif query == FlickrQuery.geotagged_flooding_tags:
        params['has_geo'] = 1
        params['tags'] = FLOODING_TAGS_DE

    else:
        raise Exception('invalid params name')
        # thun_params = dict()
        # thun_params['tags'] = tags
        # thun_params['lat'] = 47.566667 # 46.76
        # thun_params['lon'] =  7.6 # 7.624
        # thun_params['radius'] = RADIUS
        # params_list.append(thun_params)
    return params