#!/usr/bin/env bash

rm -f ~/.server/app.db
rm -rf ~/.server/logs
rm -rf ~/.server/store
rm -rf ./migrations    
mkdir ~/.server/store

# source ~/.venvs/web/bin/activate
export FLASK_APP=server.py
flask db init
flask db migrate -m "start"
flask db upgrade
deactivate
