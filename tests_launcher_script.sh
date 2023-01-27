#!/bin/bash
echo Project Testing...
coverage run --omit='*/venv/*' --omit='*/tests/*'  manage.py test 
echo ----------------------------------------------- 
echo

echo Producing the tests\' HTML Report...
coverage html
echo ----------------------------------------------- 
echo

echo Report:
coverage report 

echo Cleaning Test Files...
python3 cleaning_procedure.py

echo Done!
echo vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
echo
echo See the Test-Report in: ./htmlcov/index.html
echo