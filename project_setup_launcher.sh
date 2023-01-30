#!/bin/bash
if [ -e venv ]
then
	echo
	echo "The virtual environment it's already been created!"
	echo
else
	echo "Creating the virtual environment:"
	python3 -m venv venv
	echo "- virtual environment created"
	source ./venv/bin/activate
	echo "- virtual environment activated"
	echo

	echo "Installing dependencies:"
	python3 -m pip install --upgrade pip
	echo "-----------------------------------------------" 
	echo "- python package-management system updated"
	echo
	pip install -r requirements.txt
	echo "-----------------------------------------------" 
	echo "- dependencies installed"
	echo
fi
