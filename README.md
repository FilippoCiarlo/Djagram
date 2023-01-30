
# Social
Instagram inspired website where the photo sharing and the interaction with them are at the core of the website functionalities.

### Setup
1. Create a virtual environment<br/>
	<code>python3 -m venv venv_test</code>

2. Activate the  virtual environment<br/>
	<code>source venv_test/bin/activate</code>

3. Upgrade the Python package-management system<br/>
	<code>python3 -m pip install --upgrade pip</code>

4. Install the dependencies<br/>
	<code>pip install -r requirements.txt</code>

> To deactivate the  virtual environment run the following command:<br/>
	<code>deactivate</code>
---


### Run the Website
1. Applying unapplied migrations<br/>
<code>python3 manage.py migrate</code>

2. Run the local development server<br/>
<code>python3 manage.py runserver</code>
---


### Run the Tests
#### 1st Way
Run the BASH script present in the project folder:<br/>
<code>bash ./tests_launcher_script.sh</code>

The script will execute the following commands:
> Test all Project<br/>
<code>coverage run --omit='*/venv/*' --omit='*/tests/*'  manage.py test</code> 

> Print in the shell a report about the tested-code coverage<br/>
<code>coverage report</code>

> Make an HTML report about the tested-code coverage in the <code>./htmlcov</code> folder<br/>
<code>coverage html</code>

> Clean all media files produced during the tests execution<br/>
<code>python3 ./cleaning_procedure.py</code>

#### 2nd Way
Test all Project:<br/>
<code>python3 manage.py test</code>

- Test <code>accounts</code> application<br/>
<code>python3 manage.py test accounts</code>

- Test <code>posts</code> application<br/>
<code>python3 manage.py test posts</code>

After running the tests run the source file of the cleaning procedure, present in the project folder, to clean up all media files produced during the tests execution.
<code>python3 ./cleaning_procedure.py</code><br/>

---


### Dependencies
The code use the following dependencies:
* <code>django-environ</code>: Manages Environment Variables
* <code>pillow</code>: Manages Image 
* <code>django-taggit</code>: Handles tagging functionalities 
* <code>django-crispy-forms</code>: Makes forms look better
* <code>crispy-bootstrap5</code>: Provides Bootstrap template pack for <code>django-crispy-forms</code>
* <code>coverage</code>: Helps tracking the executed code during tests
---


### Test Database
The administrator credentials are in <strong>bold</strong>

Users Credentials:
|username|password|
|--------|---------|
|<code><strong>filippociarlo</strong></code>|<code><strong>testpass123</strong></code>|
|<code>JohnDoe</code>|<code>testpass123</code>|
|<code>JaneDoe</code>|<code>testpass123</code>|




