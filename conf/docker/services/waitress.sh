#!/usr/bin/env bash

source /project/conf/scripts/runner.sh

run_python_script "Collecting static files" "manage.py collectstatic --noinput --verbosity 0"

echo " > Initializing SERVER"
echo ;
echo "########################################################################"
echo ;
waitress-serve --port="$PORT" project.wsgi:application
