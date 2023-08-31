#!/usr/bin/env bash

rm -rf ~/Data/web/website/logs/
rm -rf ~/Data/web/website/store/
rm -rf ./migrations    

mkdir -p ~/Data/remote-electric-lab/website/logs/
mkdir -p ~/Data/remote-electric-lab/website/store/

source ~/.venvs/web/bin/activate
export FLASK_APP=./website.py
flask db init
flask db migrate -m "start"
flask db upgrade
deactivate
