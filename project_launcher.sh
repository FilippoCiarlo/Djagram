#!/bin/bash
if [ -e venv ]
then
	source ./venv/bin/activate
    echo "Applying the unapplied migrations:"
	python3 manage.py migrate
	echo "-----------------------------------------------" 
	echo
	echo "Running the local development server:"
	python3 manage.py runserver
else
    bash project_setup_launcher.sh
    bash project_launcher.sh
fi


