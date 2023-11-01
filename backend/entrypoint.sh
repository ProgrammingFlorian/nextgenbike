#!/bin/bash
cd /app/server/
flask db upgrade
flask run --host=0.0.0.0 --port=80