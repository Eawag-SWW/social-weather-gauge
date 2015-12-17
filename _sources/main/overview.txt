Overview
========
This project contains Python code to analyze Flickr and Twitter data. The motivating goal was to determine, how well one can approximate traditional wheater measurement with data derived from social media. But the code is also usable to analyze other topics. 

The main structure of the code looks like this:

.. image:: ../img/code-diagram.png

That is, if you want to run an analysis and get some diagram drawn, you have to work with functions in either ``flickr_analysis`` or ``twitter_analysis``. They get the data from the ``store``, which either downloads new data or retrieves it from the cache on disc (folder ``store_room``). If the ``store`` needs new data, it uses either ``flickr_api`` or ``twitter_api`` to access the apis of Twitter and Flickr.   






Shortcomings
------------ 