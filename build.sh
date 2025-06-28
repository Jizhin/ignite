#!/usr/bin/env bash

python manage.py migrate --no-input
gunicorn ignite_project.wsgi:application