#! /bin/sh

. env_planbiene/bin/activate
gunicorn --reload app:api
