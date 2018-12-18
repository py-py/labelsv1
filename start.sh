#!/usr/bin/env bash

rm db.sqlite3
rm ./project/media/*
rm ./project/media/images/*
python manage.py migrate
python manage.py add_superuser
python manage.py fake_data
