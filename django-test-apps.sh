#! /bin/bash

# run from cli by . django-test-apps.sh
# ensure that executable by chmod +x django-test-apps.sh



DJANGO=/Documents/code/django/mysite/

APP=polls

cd $HOME$DJANGO

coverage run --source='.' manage.py test $APP
coverage report

cd $HOME$DJANGO
