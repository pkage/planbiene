#! /bin/sh

. env_planbiene/bin/activate
gunicorn --timeout 300 --reload app:api
