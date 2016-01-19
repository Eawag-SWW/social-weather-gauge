Introduction
============
|project| is a Python library made to analyze Flickr and Twitter data. The motivating goal was to determine, how well one can approximate traditional wheater measurement with data derived from social media. But the code is also usable to analyze other topics. 

As an example, let us consider precipitation in London. |project| can download all tweets from London using the official Twitter REST-API for the last 10 days (that is the maximum you get via the API). It then caches this data on disc (in folder ``store_room``) for later reuse (see module ``main.store``). After caching the tweets get tokenized and stemmed (normalized) and compared with predefined keywords for the given topic (in this case: rain). This leads to a proportion of topic-positive tweets which then gets plotted. 

The following (and more) libraries are used:

- Pandas for Data Analysis
- Matplotlib and Seaborn for plotting
- Flickrapi to connect to the Flickr API
- Tweepy for Twitter
- NLTK for Natural Language Processing


Shortcomings
------------ 
The Twitter part could not get finished during the project run time. Therefore a few thing are yet to be implemented. But there should not be too much work needed to get it to a working state. 

- Detecting tweet language and use appropriate topic language. (The class ``Topic`` is able to handle multiple languages in principle.)
- Twitter data is restricted to the last ca. 9 days due to restriction from the Twitter API
- When querying tweets for a place, Twitter returns not much data. This is probably due to little use of geolocation from Twitter users. It could be possible to get more tweets when considering additionally the location of the user (in comparison to just use the location of the tweet).

