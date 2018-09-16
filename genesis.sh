#!/usr/bin/env bash

echo -e "Hello, welcome to Django! \n"


############# Rename app ############
echo -e "Giving App a Name..."
read -p "App Name: (djangounchained): " app_name

if [ -d $PWD"/djangounchained" ]
then
    ### Rename references inside root app
    find djangounchained/. -type f -name '*.py' -print0 | xargs -0 sed -i s/djangounchained/${app_name}/g

    ### Rename references in manage.py file
    find manage.py -type f -name '*.py' -print0 | xargs -0 sed -i s/djangounchained/${app_name}/g

    ### Rename folders
    mv djangounchained ${app_name}
    mv templates/djangounchained templates/${app_name}
fi


############ Create virtual environment and install dependencies ############
echo "Creating virtual environments..."

venv_path=$PWD"/../venv"

if [ -d ${venv_path} ]; then
    rm -rf ${venv_path}
fi

python -m virtualenv ${venv_path}

source ${venv_path}/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt


############# Manipulate .env ############
echo -e "Creating .env file..."
if [ ! -f $PWD"/.env" ]; then
    cp ./.env.example ./.env
fi

### Generate secret
python manage.py generate_secret --genesis

### Set database credentials
read -p "Database Host (127.0.0.1): " database_host
database_host=${database_host:-127.0.0.1}
sed -i -E "s/DB_HOST=.*?/DB_HOST=${database_host}/g" ./.env

read -p "Database Port (5432): " database_port
database_port=${database_port:-5432}
sed -i -E "s/DB_PORT=.*?/DB_PORT=${database_port}/g" ./.env

read -p "Database Username (postgres): " database_username
database_username=${database_username:-postgres}
sed -i -E "s/DB_USERNAME=.*?/DB_USERNAME=${database_username}/g" ./.env

read -p "Database Password (secret): " database_password
database_password=${database_password:-secret}
sed -i -E "s/DB_PASSWORD=.*?/DB_PASSWORD=${database_password}/g" ./.env

read -p "Database Name (djangounchained): " database_name
database_name=${database_name:-djangounchained}
sed -i -E "s/DB_DATABASE=.*?/DB_DATABASE=${database_name}/g" ./.env

read -p "Database Schema (djangounchained): " database_schema
database_schema=${database_schema:-djangounchained}
sed -i -E "s/DB_SCHEMA=.*?/DB_SCHEMA=${database_schema}/g" ./.env
