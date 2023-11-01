#!usr/bin/env bash
flask db upgrade
flask run --host=0.0.0.0 --port=8000