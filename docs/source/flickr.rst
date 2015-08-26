Flickr
======

* Created by Ludicorp in 2004
* Acquired by Yahoo in 2005
* 6 billion images in 2011 (we)
* 87 million registred users in 2013 (we)
* 3.5 million new images daily in 2013 (we)
* Written in PHP


API
---
* REST endpoint: https://api.flickr.com/services/rest/
* Return formats: XML, JSON, ...
* Parameters: method, api_key, format

flickr.photos.search
^^^^^^^^^^^^^^^^^^^^
Parameters:
* woe_id: A 32-bit identifier that uniquely represents spatial entities
* place_id: A Flickr place id

Response structure:
- photos
    - page
    - pages
    - perpage
    - photo
        - id
        - latitude
        - longitude 
        - place_id
        - title
        - woeid 

flickr.places.getInfo
^^^^^^^^^^^^^^^^^^^^^
Get informations about a place.
Parameters:
* woe_id
* place_id

response structure:

rsp > place > country
            > shapedata > polylines > polyline
                        > urls > shapefile

Attributes:
rsp: stat
place: place_id, woeid, latitutude, longitude, place_url, place_type, place_type_id, timezone, name, woe_name, has_shapedata
country: place_id, woeid, latitutde, longitude, place_url
shapedata: created, alpha, count_points, count_edges, has_donuthole, is_donuthole


woe id vs place id
^^^^^^^^^^^^^^^^^^
WOE = where on earth

Python Library
--------------
We use the library called flickrapi. Documentation: http://stuvel.eu/media/flickrapi-docs/documentation/
      
