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

### Setting Up
Once inside the virtual environment, make sure to have postgresql installed on your computer.
Create a database named `jobapplications` and grant any of your psql users permissions to it.

To do this:
* `sudo -u postgres psql` to connect to the database;
* `CREATE USER potato WITH PASSWORD 'potato_pw';` to create a user;
* `grant all privileges on database jobapplications to potato;` to grant the user privileges;

Next, you'll want to set your environment variables to contain the database log-in credentials:
* `export PSQL_USER="potato"`
* `export PSQL_PW="potato_pw"`

Finally, you can create the tables in your database using the `setup.py` script.
* `python setup.py`

You now have an instance of the database with the correct tables and columns! :tada:

### Upgrading
When modifying the database, alembic is in place to handle data migrations from an old schema to a new one. Alembic handles data migrations automatically, so it is sufficient to perform the following commands:
* Create the directory `alembic/versions` if it does not exist yet.
* `alembic revision -m <your message here>` to create a baseline migration (if the folder `alembic/versions` is empty and no previous migrations exist)
* `alembic upgrade head` to upgrade the database to the newest revision
* `alembic revision --autogenerate -m <your message here>` to auto generate a new version

Note that sometimes Alembic auto generates the upgrade scripts with the table deletions in the wrong order. If you see an error message containing `table <...> depends on <...>`, simply modify the python script in `alembic/versions` for your current migration to ensure it is deleting tables with the most dependencies last. 

