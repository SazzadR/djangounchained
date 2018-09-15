#!/usr/bin/env bash

echo -e "Hello, welcome to Django! \n"


############ Rename app ############


############ Create .env file ############
echo -e "Creating .env file... \n"
if [ ! -f $PWD"/.env" ]; then
    cp ./.env.example ./.env
fi
### Generate secret
python manage.py generate_secret --genesis
