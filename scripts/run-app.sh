#!/bin/bash
# scripts/run-app.sh -- Command to run the app on Heroku

if [[ -n "${QUOTAGUARDSTATIC_URL}" ]];
then
    bin/qgtunnel gunicorn -t 180 -w 3 --log-level debug asset_dashboard.wsgi:application;
else
    gunicorn -t 180 -w 3 --log-level debug asset_dashboard.wsgi:application;
fi
