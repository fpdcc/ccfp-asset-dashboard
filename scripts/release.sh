#!/bin/bash
# scripts/release.sh -- Commands to run on every Heroku release

set -euo pipefail

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py createcachetable && python manage.py clear_cache

# Check to see if data needs to be loaded for the Project table.
if [ `psql ${DATABASE_URL} -tAX -c "SELECT COUNT(*) FROM asset_dashboard_project"` -eq "0" ]; then
   python manage.py load_development_data
fi