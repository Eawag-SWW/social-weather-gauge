Install
=======

It is suggested to run SocialWeatherGauge with the Anaconda Python distribution and use its package manager ``conda`` for installing the requirements. It is possible to use another distribution and traditional, but this way is up to the user and is not described in detail.


-  Install `Anaconda <https://www.continuum.io/downloads>`__
-  Make a new conda environment called social-media-mining with

   ::

       conda env create -f .conda_requirements.yml

-  Activate this new environment with

   ::

       source activate social-media-mining

-  Clone the git repository with

   ::

       git clone https://github.com/eawag-sww/social-media-mining

-  Create a new file called ``local_config.py`` in folder ``main`` with
   the line

   ::

       ROOT_DIR = path to your root folder of the project

-  Add a file called ``secrets.py`` to folder ``main`` containing Flickr
   and Twitter API passwords:

   ::

       FLICKR_API_KEY = 
       FLICKR_API_SECRET = 
       TWITTER_CONSUMER_KEY =  
       TWITTER_CONSUMER_SECRET = 

-  To work with Twitter text, the natural language processing library
   NLTK is used. To install todo
