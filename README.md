# ALE1 project

## Description
This is a simple web app using Python and Flask that implements the functionality and requirements of the ALE1 subject

## Run the application

### First install:
1. Python (Version 3.6 was used for development)
2. pipenv (`pip install --user pipenv`)
3. Graphviz (`https://www.graphviz.org/download/`) and add `path/to/graphviz/installation/bin/` to the `PATH` variable

### Then run:
1. `pipenv install`
2. `pipenv run python run.py`

Finally go to http://localhost:5000/. Make 
sure you are connected to the Internet for the Bootstrap CDN to work.

## Run the tests

1. Open a terminal in the root directory of the project
2. Run `coverage run -m unittest discover src/tests`
3. To generate nice html output of the tests run `coverage html`
4. Navigate to folder `htmlcov` that was just generated and open `index.html`
