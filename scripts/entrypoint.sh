#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --socket :8000 --master --enable-theads --module Butchery.wsgi


