#!/bin/bash
if [ -e venv ]
then
	echo "Testing the project..."
	coverage run --omit='*/venv/*' --omit='*/tests/*'  manage.py test 
	echo "-----------------------------------------------" 
	echo
	echo "Report:"
	coverage report 
	echo "Making the HTML tested-code coverage report..."
	coverage html
	echo "-----------------------------------------------" 
	echo
	echo "Cleaning Test Files..."
	python3 ./cleaning_procedure.py
	echo "Done!"
	echo "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
	echo
	echo "See the Test-Report in: ./htmlcov/index.html"
	echo
else
	bash project_setup_launcher.sh
	source ./venv/bin/activate
	bash project_tests_launcher.sh
fi 