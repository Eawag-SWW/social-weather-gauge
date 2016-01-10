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

| photos > photo

| photos: page, pages, perpage, total
| photo: id, latitude, longitude, place_id, title, woeid 

flickr.places.getInfo
^^^^^^^^^^^^^^^^^^^^^
Get informations about a place.
Parameters:

* woe_id
* place_id

response structure:

| rsp > place
| place > country
| country > shapedata
| shapedate > polylines, urls
| polylines > polyline
| urls > shapefile

| rsp: stat
| place: place_id, woeid, latitutude, longitude, place_url, place_type, place_type_id, timezone, name, woe_name, has_shapedata
| country: place_id, woeid, latitutde, longitude, place_url
| shapedata: created, alpha, count_points, count_edges, has_donuthole, is_donuthole

flickr.places.find
^^^^^^^^^^^^^^^^^^
Returns a list of place objects for a given query string.

Parameter: query

Response:
| rsp > places
| places > place*

| rsp: stat
| places: query, total
| place: place_id, woeid, latitude, longitude, place_url, place_type 

woe id vs place id
^^^^^^^^^^^^^^^^^^
WOE = where on earth

Python Library
--------------
We use the library called flickrapi. Documentation: http://stuvel.eu/media/flickrapi-docs/documentation/

Twitter
=======

Basics
------

- 140 Characters per tweet
- 1.9 million tweets January 2009 (twitter api: up and running, p.4)
- 340 milion tweets each day (2012)
- launched July 2006
- Twitter Inc in San Francisco


API
---

Schema Tweet::

   id
   lang
   text 
   created_at
   coordinates
      [coordinates]
   place
   entities
      [hashtags]
         text
      [urls]

Schema Place::

   bounding_box 
      [coordinates]
         [float]
      type
   contained_within
   country
   country_code
   full_name
   name
   place_type
   geometry 



REST-api
^^^^^^^^

https://api.twitter.com/{version}

Search
^^^^^^

The Search API is not complete index of all Tweets, but instead an index of recent Tweets.
At the moment that index includes between 6-9 days of Tweets. (https://dev.twitter.com/rest/public/search)


Tweepy
------

Python library used to connect to Twitter API through python.

Schema Place
    full_name

Schema Status streaming-api:
    contributors
    truncated
    text
    in_reply_to_status_id
    id
    favorite_count
    author
        User
        follow_request_sent
        profile_use_background_image 
    _json
        follow_request_sent
        profile_use_background_image
        default_profile_image
        id
        verified
        profile_image_url_https
        profile_sidebar_fill_color

API
^^^

- API.rate_limit_status (http://docs.tweepy.org/en/v3.2.0/api.html#API.rate_limit_status)

Response Schema::

    {
        rate_limit_context 
            access_token
        resources 
            *resource_type*
                *resource_name*
                    limit
                    remaining
                    reset
    }   
  
    
    
***********       
Geolocation
***********

- tweet is geotagged by user
- in germany 1% of tweets are geotagged
- Approximately 3-5% of all tweets are geo-enabled (https://github.com/Ccantey/GeoSearch-Tweepy)
- induce location from user profile
- induce location from tweet text
      
