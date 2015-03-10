import api
from api import flickr


def tags_for_place(woe_id):
    response = flickr.places.tagsForPlace(woe_id=woe_id)
    print(response)


def find_place(query):
    response = flickr.places.find(query=query)
    print(response)


def sandbox():
    params = api.get_params('switzerland')
    photos = api.get_photos(params) 
    print photos.get_size()


sandbox()
