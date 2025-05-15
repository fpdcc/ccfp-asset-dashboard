# CIP Planner and Asset Dashboard application

## Developing

Development requires a local installation of [Docker](https://docs.docker.com/install/)
and [Docker Compose](https://docs.docker.com/compose/install/).

Build application containers:

```
docker-compose build
```

Run the app:

```
docker-compose up
```

The app will be available at http://localhost:8000. The database will be exposed
on port 32001.

Load the development data:
```bash
docker-compose run --rm app python manage.py loaddata asset_dashboard/fixtures/data.json
```

Import the district boundaries:
```bash
docker-compose run --rm app make districts
```

### Restore the FPDCC database
Download the database from Dropbox and save the tar file in this repo's root directory. You'll need to have postgres installed on your machine to run the command.

Load the database:
```
pg_restore -U postgres -h localhost -p 32002 -d fpdcc -O FPDCC_DataMade_backup112221.tar
```

The password is `postgres` (as defined in `docker-compose.yml`).

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

### Debugging
Run the app with a debugger:
```
docker-compose run --rm -p 8000:8000 app
```

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

## Tech Stack
This application is a Django app with Postgres. It's managed with Docker. Parts of the user interface were built with React (such as all map interfaces and the CIP planner page).

You'll need Docker on your machine for local development, otherwise Docker will take care of all the dependencies. Read [DataMade's how-to documentation](https://github.com/datamade/how-to/blob/main/docker/local-development.md) for details on the Docker configuration.

The React code is baked into the Django templates. Read more about this approach in [DataMade's documentation about Django/React integration](https://github.com/datamade/how-to/blob/main/django/django-react-integration.md).

## How to Deploy
This application is deployed via AWS CodeDeploy and is hosted on EC2 instances owned by CCFP. The pipeline is setup so that the `master` branch deploys to the staging site, and the `deploy` branch deploys to the production site.

There are a few ways to prompt a deployment:
1. Whenever code is pushed to GitHub and merged to `master`, CodeDeploy will automatically deploy the `master` branch to the staging environment. 
    - You can prompt this by merging a pull request, or you can push your local `master` to GitHub (`git push origin master`). Once your master branch is ready for production, you can deploy to production from your local command line with this command: `git push origin master:deploy`. This resets the `deploy` branch to mirror `master`, which initiates the deploy action. **This is the preferred way to deploy.**

2. Via the AWS dashboard's user interface. You'll only ever do this in the rare case that the GitHub/CodeDeploy integration is broken. This may have happened because the user previously assigned to deployments no longer has access to the repo. Currently the user assigned to both production and staging is "xmedr". To fix this:
    - Log in to CCFP's AWS instance (url and credentials found in Bitwarden under `CCFP Forest Preserve of Cook County AWS creds`)
    - Go to CodeDeploy > Applications > ccfp-asset-dashboard > either production or staging > Create Deployment
    - Select the option "My Application is stored on GitHub"
    - Enter a new GitHub token name (GitHub username), the repository name, and the full commit id of the latest commit in the branch you're looking to deploy (can be found in the commit's url)
    - Every other option can be left as is. Click Create Deployment, and you're done!

3. [Using the AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/deploy/create-deployment.html). You'll only ever do this in the rare case that the GitHub/CodeDeploy integration is broken.

At time of writing, the AWS environment is not set up to have review apps.

## Details about how databases are connected
The application uses two databases:
1. A Postgres instance on AWS RDS. This is the application's main database that we write to.
    - The RDS instance is named `asset-dashboard`. We created two databases within the instance: `production` and `staging`.
    - Each app for the CIP dashboard in EC2 is configured to connect with the corresponding environment's database.
    - When we were hosting this on Heroku, the RDS security group had to be configured to accept connections from the application on Heroku. Since Heroku doesn't have static IP addresses, the [quotagaurd static add-on](https://elements.heroku.com/addons/quotaguardstatic) helped establish a connection with the remote database. For details on how that worked, see [PR #91](https://github.com/fpdcc/ccfp-asset-dashboard/pull/91) and [PR #70](https://github.com/fpdcc/ccfp-asset-dashboard/pull/70), as well as discussions in issues [#59](https://github.com/fpdcc/ccfp-asset-dashboard/issues/59) and [#60](https://github.com/fpdcc/ccfp-asset-dashboard/issues/60).

2. The Forest Preserves of Cook County's GIS database. We've setup a remote connection with the FPDCC's database. This connection also required QuotaGuard Static.

## What you can set in admin account
In the admin interface located on the website path `/admin`, an admin user can do these things:
- create/modify/delete user accounts
- create/modify/delete project categories and sections
- create/modify/delete projects (though this is an inferior way compared to the standard project detail page outside of the admin interface — only use this to delete project)
- change the score weights for the project scoring
- add users as "staff" and assign the staff to a specific section

## Where to find things in the code

### Models
All of the models are in the `asset_dashboard/models.py` file. We're using two types of models: [managed and unmanaged models](https://docs.djangoproject.com/en/3.2/ref/models/options/#managed). All of the models that inherit from the standard Django `models.Model` class are readable and writeable — these are managed models. The ones that inherit from the `GISModel` class are readable and are unmanaged. These unmanaged models allow us to use the Django ORM so that we can access the Forest Preserves' GIS database.

### Views
This application uses both standard Django class views, as well as the Django Rest Framework for JSON and GeoJSON. The views are located at:
- `asset_dashboard/views.py`
- `asset_dashboard/endpoints.py`

### URLS
`asset_dashboard/urls.py` contain the URLS that are connected to the Django views and DRF endpoints.

### Serializers and Forms
The forms that are within HTML use the Django form classes, and they're located at `asset_dashboard/forms.py`. These forms are served up in the views.

The Django Rest serializers are located at `asset_dashboard/serializers.py`. These serializers are only used with the `asset_dashboard/endpoints.py` file. Together, these pieces of the Django Rest Framework manage ajax requests from the React code. **Any GET or POST requests in the React code happen outside of the typical Django view/template and are managed on the backend with Django Rest Framework.**

### React
As mentioned, parts of this codebase use React. You'll need to dive into the React code if you're dealing with anything related to the maps and CIP planner. All of the React code is located in `asset_dashboard/static/js`.

The CIP planner is located in the `~/js/PortfolioPlanner.js` file (and you should be able to find all of the component's local imports through that).

The relevant map components are located in:
- `~/js/components/maps/SelectAssetsMap.js` — this component manages everything about searching for assets, saving/deleting assets for a phase, and copying assets to a new phase. This is the component that renders on that site at the url `<site-name>.com/projects/phases/edit/<phase_id>/assets/`. [The code is "embedded" within the template located at `~/templates/asset_dashboard/asset_create_update.html`](https://github.com/fpdcc/ccfp-asset-dashboard/blob/master/asset_dashboard/templates/asset_dashboard/asset_create_update.html#L22-L33).
- `~/js/components/PhaseDetailAssetTable.js` - this component shows a read-only map and table with assets for a phase. It also manages whether or not a phase is "countywide". The component will render in a phase's detail page: `templates/asset_dashboard/partials/forms/add_edit_phase_form.html`.
- ~/js/components/ProjectDetailAssetTable.js` - this component shows a read-only map with assets for a project/phase. If a project has assets, it will render in the project's detail page: `asset_dashboard/templates/asset_dashboard/project_detail.html`

For understanding this Django/React integration, see [the DataMade documenation about that](https://github.com/datamade/how-to/blob/main/django/django-react-integration.md). Reading that documentation will help you understand how the React is packaged within the Django template's HTML, as well as how you'll be able to use the Django views to pass data to React.

### Templates
All of the HTML is located in `asset_dashboard/templates` directory.

### Static
All JavaScript and CSS is contained in the `asset_dashboard/static` directory.

## Management commands
You'll be able to use any of the built-in Django management commands, but you'll need to do it within the Docker container. For example, to create a new migration, you'll do: `docker-compose run --rm app python manage.py makemigrations`.

We've created some extra commands, located in `asset_dashboard/management/commands`.
1. `clear_cache.py` automatically runs whenever a new version of the app deploys.
2. Create the zones and political boundaries. These all run whenever the application deploys, but also need to be ran when developing locally (as documented in the README with the `docker-compose run --rm app make districts` command). These are orchestrated with a Makefile and should be ran together.
  - `create_zone_geojson.py` creates the zone boundaries based on the GIS database.
  - `import_boundaries.py` creates political boundaries from public data
3. `load_development_data.py` loads some fake data for local development. This is documented in the README steps for setting up local development.

## Docker commands
See above development section for when setting up the application for local development.

Some other helpful docker commands:
- `docker-compose run --rm app python manage.py shell` enters the Django shell
- `docker-compose run --rm app bash` enters a bash session in the Docker container

