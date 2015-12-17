# Social Media Mining For Weather Data

Be aware: This project is not finished yet and contains unstable code which can contain bugs or not yet implemented functionality.

## Overview

This project contains Python code to analyze Flickr and Twitter data. The motivating goal was to determine, how well one can approximate traditional wheater measurement with data derived from social media. But the code is also usable to analyze other topics. 



- Install anaconda (https://www.continuum.io/downloads)
- make a new conda environment called social-media-mining with::

    conda env create -f .conda_requirements.yml

- activate this new environment with::

    source activate social-media-mining

- download source code from git ...
- create new file called local_config.py in folder main with the line

    ROOT_DIR = path to you the root folder of the project

- add a file called `secrets.py` to folder `main` containing constants
    todo

- add a file called `local_config.py` to folder `main` defining constant
    todo

- download nltk tokenizers


## Logging
-------
activate logging...


## Documentation
-------------
Project documentation is in the `docs` folder.

Documentation gets deployed as a website on http://dominiclooser.github.io/social-media-mining/
via the bash script `deploy-docs` in the projects root directory.
