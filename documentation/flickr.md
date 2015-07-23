
Flickr
======

- Created by Ludicorp in 2004
- Acquired by Yahoo in 2005
- 6 billion images in 2011 (we) 
- 87 million registred users in 2013 (we) 
- 3.5 million new images daily in 2013 (we)    
- Written in PHP

All following data concern just geotagged photos.

Number of photos geotagged with Switzerland: 2'451'335
Swiss / tags =


API
---
- REST endpoint: https://api.flickr.com/services/rest/
- Return formats: XML, JSON, ...
- Parameters: method, api_key, format 

### flickr.photos.search

Parameters:
- woe_id: A 32-bit identifier that uniquely represents spatial entities
- place_id: A Flickr place id 



Response structure:

photos
   page
   pages
   perpage
   photo
      [
      id
      latitude
      longitude 
      place_id
      title
      woeid 
      ]
stats









