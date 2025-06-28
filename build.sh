#!/usr/bin/env bash

python manage.py migrate --fake-initial --no-input
gunicorn ignite_project.wsgi:application