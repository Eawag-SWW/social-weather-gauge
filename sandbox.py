
from api import api
import constants


def tags_for_place(woe_id):
    response = api.places.tagsForPlace(woe_id=woe_id)
    print(response)

def find_place(query):
    response = api.places.find(query=query)
    print(response)



find_place('Schweiz')
