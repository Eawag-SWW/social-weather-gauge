% Wheater Measurement Through Social Media Data Mining: Report
% Dominic Looser

Background
==========

Flickr
------
- Created by Ludicorp in 2004
- Acquired by Yahoo in 2005
- 6 billion images in 2011 (we) 
- 87 million registred users in 2013 (we) 
- 3.5 million new images daily in 2013 (we)    
- Written in PHP

interesting numbers:
- number of photos total
- number of photos per region / year / geotagged


Twitter
-------

Implementation
==============



Python 2.7

Important Libraries
---
- Pandas (data analysis)
- Matplotlib/Seaborn (plotting)
- flickrapi
- tweepy
- nltk (natural language processing)

Modules
---
- apis/flickr_api.py: Classes and functions which abstract over the flickr api.
- apis/twitter_api.py: Defines important classes Tweet, TwitterSearchQuery, and TwitterStreamingQuery. Enable downloading tweets for search queries and to start streaming with filtering according to a given TwitterStreamingQuery. 
- all api modules need secret keys which are defined in secrets.py (not checked in into git)
- geo.py: Enables to plot data on a map. Uses basemap matplotlib extension. Defines constants for used bounding boxes.  
- store.py: Enables caching of downloaded data through apis. Different store types are defined in instances of class StoreType, e.g. SEARCH_TWEETS or FLICKR_PLOT. When using functions that use social media data (e.g. for plotting), one can use the option use_cache in order to work with data stored on disc rather than downloading it again.
- 


Results
===

Flooding
---

Rain
---


