#!/bin/bash
echo Applying the unapplied migrations:
python3 manage.py migrate
echo ----------------------------------------------- 
echo

echo Running the local development server:
python3 manage.py runserver
