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

- rest-api vs. streaming api

.. http:get:: geo/id/:place_id

   `docs <https://dev.twitter.com/rest/reference/get/geo/id/%3Aplace_id>`_

   response format::

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
schema: 

- text 
- created_at
- coordinates
- place
- entities
    - hashtags
        - text

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