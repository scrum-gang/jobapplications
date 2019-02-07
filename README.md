# Job Applications
Repository for the microservices which enables users to track their job applications.

Job applications can either come from a user submitting the application form of a in-house posting, or simply by tracking an external posting via our platform.

This is currently a work in progress, the [database schema can be found here](https://github.com/scrum-gang/jobapplications/wiki/Database-Design).

# Setup

Note: This service uses Python 3.6 or higher. Use lower versions at your own risk ...
Also, the setup guide assumes you are running a bash terminal.

## API

To run the microservice, you need to...

* ... create a virtual python environment using the following command: `python -m venv venv`
* ... activate the environment: `source venv/bin/activate`
* ... install the dependencies: `pip install -r requirements.txt`
* ... run the API :tada: : `python app.py`

## Database

Once inside the virtual environment, make sure to have postgresql installed on your computer.
Create a database named `jobapplications` and grant any of your psql users permissions to it.

To do this:
* `sudo -u postgres psql` to connect to the database;
* `CREATE USER potato WITH PASSWORD 'potato_pw';` to create a user;
* `grant all privileges on database jobapplications to potato;` to grant the user privileges;

Next, you'll want to set your environment variables to contain the database log-in credentials:
* `export PSQL_USER="potato"`
* `export PSQL_PW="potato_pw"`

Finally, you can create the tables in your database using the `setup.py` script. Note that this
script is temporary and will be replaced with proper migrations using `alembic` shortly!
* `python setup.py`

You now have an instance of the database with the correct tables and columns! :tada:
