


# Local

API:

DATABASE_URL=postgresql://:@localhost/mlm_transcriptions apistar run

CLIENT:

npm run serve


# Production

API:

Running with gunicorn under supervisord.

Proxied via NGINX


CLIENT:

Created distribution files with npm run build. Served with NGINX.


# DB

To build databases from CSV


csvsql --db sqlite:///leso.db --insert joined.csv

csvsql --db sqlite:///leso.db --insert joined.csv


