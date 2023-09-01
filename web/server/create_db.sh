#!/usr/bin/env bash

rm -rf ~/Data/webdeprecios
rm -rf ./migrations    

source ~/.venvs/web/bin/activate
python ./create_storage_webdeprecios.py
export FLASK_APP=./server.py
flask db init
flask db migrate -m "start"
flask db upgrade
deactivate
