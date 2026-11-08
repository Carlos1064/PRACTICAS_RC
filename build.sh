#!/usr/bin/env bash
set -o errexit

python -m pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --noinput
python manage.py bootstrap_admin

if [[ "${LOAD_DEMO_DATA:-}" == "true" ]]; then
    python manage.py seed_demo
fi
