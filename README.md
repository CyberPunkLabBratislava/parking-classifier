# Instructions for running the AI app
## Run for localhost only
* Create and activate python 3 venv within the project folder:
    ~~~~
    python3 -m venv .
    source bin/activate
    ~~~~
* Install packages and module
    ~~~~ 
    pip install .
    ~~~~
* Run the tool    
    ~~~~
    parking_classifier -d <Your project path>
    ~~~~

## Run with docker
* Build the project
    ~~~~
    ./build.sh
    ~~~~
* Run the docker image parking-classifier

## Run as linux service
TBD