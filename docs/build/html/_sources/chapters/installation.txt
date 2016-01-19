Installation
============

It is suggested to run |project| with the Anaconda Python distribution and use its package manager Conda for installing the requirements. It is possible to use another distribution and traditional pip for package management, but this way is up to the user and is not described here.

Proceed with following steps:

-   Install `Anaconda <https://www.continuum.io/downloads>`__
-   Make a new conda environment called ``swg`` (standing for |project|) with ::

        conda env create -f .conda_requirements.yml

    The file ``.conda_requirements.yml`` lists all required packages and these get installed in a new conda environment.

-   Activate this new environment with ::

        source activate swg

-  Clone the git repository with ::

       git clone https://github.com/eawag-sww/social-media-mining

-  Create a new file called ``local_config.py`` in folder ``main`` with
   the line ::

       ROOT_DIR = path to your root folder of the project

-  Add a file called ``secrets.py`` to folder ``main`` containing Flickr
   and Twitter API passwords ::

       FLICKR_API_KEY = 
       FLICKR_API_SECRET = 
       TWITTER_CONSUMER_KEY =  
       TWITTER_CONSUMER_SECRET = 

-   To work with Twitter text, the natural language processing library
    NLTK is used. Currently, only english words are stemmed, using the Porter Stemmer. This stemmer should be preinstalled with NLTK, but if it is missing you can download it (and other NLTK extensions) using ::

        import nltk
        nltk.download()

    in a python shell. 

