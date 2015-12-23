# Social Media Mining For Weather Data

Be aware: This project is not finished yet and contains unstable code which can contain bugs or not yet implemented functionality.

## Prerequisites
- Installed git and basic git knowledge

## Install

This project used the Anaconda Python distribution with its package manager conda for development. It is also possible to install it with another distribution and pip, but using Anaconda and conda should be easier and is the suggested way. 

- Install [Anaconda](https://www.continuum.io/downloads)
- Make a new conda environment called social-media-mining with
        
        conda env create -f .conda_requirements.yml

- Activate this new environment with
    
        source activate social-media-mining

- Clone the git repository with

        git clone https://github.com/eawag-sww/social-media-mining

- Create a new file called `local_config.py` in folder `main` with the line

        ROOT_DIR = path to your root folder of the project

- Add a file called `secrets.py` to folder `main` containing Flickr and Twitter API passwords:

        FLICKR_API_KEY = 
        FLICKR_API_SECRET = 
        TWITTER_CONSUMER_KEY =  
        TWITTER_CONSUMER_SECRET = 

- To work with Twitter text, the natural language processing library NLTK is used. To install 
        todo


## Logging

activate logging...


## Documentation
Documentation gets deployed on http://eawag-sww.github.io/social-media-mining/. Its source code lives in the `docs` folder.


