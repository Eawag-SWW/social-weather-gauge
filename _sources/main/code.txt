Code
========

All code is based on Python 3

Install
-------
.. highlight:: shell

- Install anaconda (https://www.continuum.io/downloads)
- make a new conda environment called social-media-mining with::

    conda env create -f .conda_requirements.yml

- activate this new environment with::

    source activate social-media-mining

- download source code from git ...
- create new file called local_config.py in folder main with the line

    ROOT_DIR = path to you the root folder of the project


Important Libraries
-------------------
* Pandas (data analysis)
* Matplotlib/Seaborn (plotting)
* flickrapi
* tweepy
* nltk (natural language processing)