import flickrapi


FORMAT = 'parsed-json'
WOE_ID_SWITZERLAND = 23424957

api = flickrapi.FlickrAPI(API_KEY, API_SECRET, format=FORMAT)
tag_options = [['hochwasser'], ['überschwemmung'], ['überflutung'], ['flut']]
woe_id = WOE_ID_SWITZERLAND
RADIUS = 30

options_dicts = []
for tag_option in tag_options:
    options = dict()
    options['tags'] = tag_option
    options['lat'] = 46.76
    options['lon'] = 7.624
    options['radius'] = RADIUS
    options_dicts.append(options)


for options_dict in options_dicts:
    response = api.photos.search(**options_dict)
    total = response['photos']['total']
    print('tags: %s, total: %s' % (options_dict['tags'], total))






# photos = result['photos']['photo']
# for photo in photos:
#     url = 'https://www.flickr.com/photos/%s/%s' % (photo['owner'], photo['id'])
#     print(url)




# answers = api.places.find(query='Switzerland')
# print(answers)
