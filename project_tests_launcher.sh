#!/bin/bash
echo Testing the project...
coverage run --omit='*/venv/*' --omit='*/tests/*'  manage.py test 
echo ----------------------------------------------- 
echo

echo Report:
coverage report 

echo Producing an HTML tested-code coverage report...
coverage html
echo ----------------------------------------------- 
echo

echo Cleaning Test Files...
python3 ./cleaning_procedure.py

echo Done!
echo vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
echo
echo See the Test-Report in: ./htmlcov/index.html
echo