Social Media Mining For Weather Data
====================================

Be aware: This project is not finished yet and contains unstable code which can contain bugs or not yet implemented functionality.

Install
-------

* Install Anaconda (https://www.continuum.io/downloads)
* Make a new conda environment called social-media-mining with::

    conda env create -f .conda_requirements.yml

* activate this new environment with::

    source activate social-media-mining

* Clone the git repository with::

    git clone https://github.com/Eawag-SWW/social-media-mining.git 

* Create a new file called ``local_config.py`` in folder ``main`` with the line::

    ROOT_DIR = path to your root folder of the project

* Add a file called `secrets.py` to folder `main` containing constants
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
