#!/bin/sh
set -e

echo "Running DB create user"
python create_initial_user.py

echo "Running api"
exec gunicorn run:app --bind 0.0.0.0:8080

