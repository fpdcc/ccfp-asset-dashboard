#!/bin/bash
# scripts/release.sh -- Commands to run on every Heroku release

set -euo pipefail

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py createcachetable && python manage.py clear_cache
python manage.py loaddata asset_dashboard/fixtures/data.json
