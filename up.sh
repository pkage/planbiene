#! /bin/sh

virtualenv env_planbiene -p python3
source env_planbiene/bin/activate
pip3 install -r requirements.txt --verbose
