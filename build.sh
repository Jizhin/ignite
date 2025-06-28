#!/usr/bin/env bash

python manage.py migrate --no-input
gunicorn your_project_name.wsgi:application