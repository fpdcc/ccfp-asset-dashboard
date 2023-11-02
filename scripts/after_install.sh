#!/bin/bash
set -euo pipefail

# Make sure the deployment group specific variables are available to this
# script.
source /home/datamade/asset-dashboard/configs/$DEPLOYMENT_GROUP_NAME-config.conf

# Set some useful variables
DEPLOYMENT_NAME="$APP_NAME-$DEPLOYMENT_ID"
PROJECT_DIR="/home/datamade/$DEPLOYMENT_NAME"
VENV_DIR="/home/datamade/.virtualenvs/$DEPLOYMENT_NAME"

# Move the contents of the folder that CodeDeploy used to "Install" the app to
# the deployment specific folder
mv /home/datamade/asset-dashboard $PROJECT_DIR

# set up the right .env file
mv $PROJECT_DIR/configs/.env.$DEPLOYMENT_GROUP_NAME $PROJECT_DIR/.env
echo -e "\nDEPLOYMENT_ID=$DEPLOYMENT_ID" >> $PROJECT_DIR/.env

# Create a deployment specific virtual environment
python3 -m venv $VENV_DIR

# Upgrade pip and setuptools. This is needed because sometimes python packages
# that we rely upon will use more recent packaging methods than the ones
# understood by the versions of pip and setuptools that ship with the operating
# system packages.
$VENV_DIR/bin/pip install --upgrade pip
$VENV_DIR/bin/pip install --upgrade setuptools

# Install the project requirements into the deployment specific virtual
# environment.
$VENV_DIR/bin/pip install -r $PROJECT_DIR/requirements.txt --upgrade

# Install JS dependencies
( cd $PROJECT_DIR && npm install )

# OPTIONAL Run migrations and other management commands that should be run with
# every deployment
(
    cd $PROJECT_DIR
    env $(cat .env | xargs) $VENV_DIR/bin/python manage.py migrate
    env $(cat .env | xargs) $VENV_DIR/bin/python manage.py createcachetable
    env $(cat .env | xargs) $VENV_DIR/bin/python manage.py collectstatic --no-input
    env $(cat .env | xargs) $VENV_DIR/bin/python manage.py compress
)

# Set the ownership of the project files and the virtual environment
chown -R datamade.www-data $PROJECT_DIR
chown -R datamade.www-data $VENV_DIR

# Echo a simple nginx configuration into the correct place, and tell
# certbot to request a cert if one does not already exist. 
# Wondering about the DOMAIN variable? It becomes available by source-ing 
# the config file (see above).
if [ ! -f /etc/letsencrypt/live/$DOMAIN/fullchain.pem ]; then
    echo "server {
        listen 80;
        server_name $DOMAIN;

        location ~ .well-known/acme-challenge {
            root /usr/share/nginx/html;
            default_type text/plain;
        }

    }" > /etc/nginx/conf.d/$APP_NAME.conf
    service nginx reload
    certbot -n --nginx -d $DOMAIN -m devops@datamade.us --agree-tos
fi

# Install Jinja into the virtual environment and run the render_configs.py
# script.
$VENV_DIR/bin/pip install Jinja2>=2.10
$VENV_DIR/bin/python $PROJECT_DIR/scripts/render_configs.py $DEPLOYMENT_ID $DEPLOYMENT_GROUP_NAME $DOMAIN $APP_NAME
