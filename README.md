# CCFP Asset Dashboard

## Collateral
https://drive.google.com/drive/u/0/folders/1bUi3QwhvpBLfcs3qSr-ttKQYrglH__oj

## Developing

Development requires a local installation of [Docker](https://docs.docker.com/install/)
and [Docker Compose](https://docs.docker.com/compose/install/).

Build application containers:

```
docker-compose build
```

Load the dummy data for development:
```
docker-compose run --rm app python manage.py load_development_data
```

Run the app:

```
docker-compose up
```

The app will be available at http://localhost:8000. The database will be exposed
on port 32001.

Run the app with a debugger:
```
docker-compose run --rm -p 8000:8000 app
```

Load the development data:
```bash
docker-compose run --rm app python manage.py loaddata asset_dashboard/fixtures/data.json
```

### Restore the FPDCC database
Download the database from Dropbox and save the tar file in this repo's root directory.

Load the database:
```
pg_restore -U postgres -h localhost -p 32002 -d fpdcc -O FPDCC_DataMade_backup112221.tar
```

Connect to the database with `psql`:
```
psql -U postgres -h localhost -p 32002
```

Examine the tables. In the postgres shell:
```
postgres=# \c fpdcc
psql (14.0, server 12.5)
You are now connected to database "fpdcc" as user "postgres".
fpdcc=# \dt *.*
```

You should see a list of all the tables.

### Compiling Sass to CSS

This project uses Sass to compile a custom Bootstrap build with house styles.
Making changes to the Sass? Use our `develop` script to auto-compile your
changes to CSS and commit your changes.

```bash
# On a running app container
docker-compose exec app npm run-script develop

# OR, in a one-off container
docker-compose run --rm app npm run-script develop

# Add your changes to version control
git add asset_dashboard/static/css/bootstrap.custom.css
git commit -m "Update custom Bootstrap build"
```

Note that you only need to update the Sass to override base Bootstrap styles.
See [the Bootstrap documentation on theming](https://getbootstrap.com/docs/4.5/getting-started/theming/)
for more information.

To extend Bootstrap styles and add new styles, edit `app.css` directly.

### Running tests

Run tests without testing the GIS models:

```
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```

To test the GIS models in your local environment with the restored database, use this command with the `TEST_GIS` environment variable:
```
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run -e TEST_GIS=True --rm app
```

### Dumping and Loading Fixture Data
Dump the data:
```bash
docker-compose run --rm app python manage.py dumpdata \
    --natural-foreign \
    --indent 2 \
    -e contenttypes \
    -e sessions \
    -o asset_dashboard/fixtures/data.json \
    asset_dashboard auth
```


