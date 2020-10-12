# Analytics Services

Analytics services use the powerful libraries in Python such as Pandas and scikit-learn to analyze the data. The services are developed using the Django Rest Framework is widely used Rest API platform in Python. It also provides in-built authentication, serialization, ORM and web browsable API view. The project demonstrates data analysis and machine learning capabilities.

[Django Framework](https://www.playframework.com/documentation/2.8.x/Home) is a lightweight, stateless and highly scalable web application framework with minimal resource consumption. Play is built on top of Akka and Akka HTTP which enables to develop lightning-fast applications. Although Play is based on MVC programming model, it also offers tools to create fully-featured REST APIs as well as plugins to support important features such as authorization, integration with databases. The Play Services demonstrates the capabilities of Play framework in developing REST services with [OAuth2 Security](https://github.com/nulab/play2-oauth2-provider), [Slick Database Framework](https://www.playframework.com/documentation/2.8.x/PlaySlick), [ReactiveMongo](http://reactivemongo.org/) and external [WebServices](https://www.playframework.com/documentation/2.8.x/ScalaWS).


### Setup PostgreSQL Server

* Download latest [Windows PostgreSQL Installer](https://www.postgresql.org/download/windows/) and follow windows installation steps.
* Alternatively, can download [Windows PostgreSQL Binary Archive](https://www.enterprisedb.com/download-postgresql-binaries) and extract the zip file. POSTGRE_SQL_HOME is the path to the unzipped PostgreSQL **pgsql** directory.
* Create `data` directory in `POSTGRE_SQL_HOME/pgsql` and initialize the postgres database using `pg_ctl init` command from [pg_ctl](https://www.postgresql.org/docs/9.5/static/app-pg-ctl.html) utility.


        $ pg_ctl -D "POSTGRE_SQL_HOME/pgsql/data" init

* Start the Posgres server in background with the initialized data directory. PostGreSQL runs by default on port 5432.


        $ pg_ctl -D "POSTGRE_SQL_HOME/pgsql/data" -l logfile start

* Create default `postgres` as superuser and set the password as `secret`.


        $ createuser --password --superuser postgres

* Alternatively, the password of `postgres` user can be changed as below after logging into psql.


        $ psql -U postgres
        postgres=#  \password
        postgres=#  ALTER USER postgres WITH PASSWORD 'new_password';

* Register Posgres server with data directory path as a windows service.


        $ pg_ctl register -N postgres -D "POSTGRE_SQL_HOME/pgsql/data"
        
* Create a new user named **appuser** and new database named **appdb** using below **psql** commands.


        $ psql -U postgres
        postgres=#  CREATE USER appuser WITH PASSWORD 'secret123';

* Create a new database `appdb` and grant all privileges for the database to user `appuser`. user named **appuser** and new database named **appdb** using below **psql** commands.


        postgres=#  CREATE DATABASE appdb;
        postgres=#  GRANT ALL PRIVILEGES ON DATABASE appdb TO appuser;
        postgres=#  \c appdb;

* Alternatively, database can be created using the [createdb](https://www.postgresql.org/docs/9.1/app-createdb.html) utility as below. Then login into psql with appuser and appdb database.


        $ createdb --owner appuser appdb
        $ psql -h localhost -U appuser -d appdb
        postgres=#  \q


* To remove the user `appuser` and database `appuser`, login into psql using `postgres` superuser and execute below drop commands.


        $ psql -U postgres
        postgres=#  DROP DATABASE appdb;
        postgres=#  DROP USER appuser;

**NOTES** 
- While running `pg_ctl.exe register` command, please ensure that the windows command prompt is running as administrator, to avoid `pg_ctl: could not open service manager` error.
- If the data directory is not initialized pg_ctl returns the error `pg_ctl: directory "C:/Installs/pgsql/data" is not a database cluster directory`.
- The `postgres` user is not created by default and hence should be created using [createuser](https://www.postgresql.org/docs/12/app-createuser.html) utility to avoid the `FATAL:  role "postgres" does not exist` error.
 

### Running Django Services

Below are the instructions to download/setup Python3, PIP, Poetry and to run Django Services using command line.

* Download the latest [Python3 Release](https://www.python.org/downloads/) and install it. It is recommended to use installer rather than standalone version for windows machine.
* Install PIP using the below command.


        $ python get-pip.py

* Install Poetry using PIP as below.


        $ pip install poetry

* Install all the python packages by reading the `pyproject.toml` file in the project directory. 
  Subsequently run all the commands with `poetry run` prefix command, in order to run them in poetry's virtual environment. 
  Run Django's `makemigrations`, `migrate` and `runserver` commands as below to setup and run django rest services.


        $ poetry install
        $ poetry run python manage.py makemigrations
        $ poetry run python manage.py migrate
        $ poetry run python manage.py runserver

* Alternatively, if want to start a fresh project `analytics-services` and create an app `api` for example, can be achieved using below commands. 


        $ poetry run django-admin startproject analytics-services
        $ poetry run django-admin startapp api


### Accessing Django Admin Page

* Create a new super user `admin` with the password `secret123`:


        $ poetry run python manage.py createsuperuser --email admin@emprovise.com --username admin

* Access the Admin page at [http://localhost:8000/admin](http://localhost:8000/admin)


### Register new user

* In order to create a new user, first login into [Admin page](http://localhost:8000/admin) using the super user credentials 
  created earlier.

* Go to sign up page at [http://localhost:8000/signup/](http://localhost:8000/signup/) and fill in the username, password, 
  email and other details. After submitting the form by clicking on post, a new user is created.

* Login at [http://localhost:8000/api-auth/login/](http://localhost:8000/api-auth/login/) with the new user.

### Register an application

To obtain a valid access_token for an application, we need to register the application. The Django OAuth Toolkit has a set of 
customizable views we can use to CRUD application instances.

   - Go to [http://localhost:8000/o/applications/](http://localhost:8000/o/applications/)
   - Click on the link to create a new application which will take to a form. Fill the form with the following data and save:
        - Name: just a name of your choice
        - Client Type: confidential
        - Authorization Grant Type: Resource owner password-based

   ![New Application Form](images/new_app_form.png)



### Testing OAuth2 using HttpPie

   - Install [HTTPie](https://httpie.org/), command-line HTTP client for the API with JSON support.


        $ pip install httpie

   - Generate a new Oauth token by calling the endpoint [http://localhost:8000/o/token/](http://localhost:8000/o/token/) and passing 
     the `client_id` and `client_secret` from the application registered above. The `username` and `password` is the user created 
     using the http://, and `grant_type` is `password`. The HTTPie's `-v` option represents verbose, while `-f` option represents 
     form request. 

    $ http -v -f POST http://localhost:8000/o/token/ 'client_id=<clientId>' 'client_secret=<clientSecret>' 'grant_type=password' 'username=admin' 'password=secret123'

    {
        "access_token": "dSCqdRi7y9wxRy4AWMh3klpgFEzBGj",
        "expires_in": 36000,
        "refresh_token": "0u3mnJBGfdTKcgLpxR6f8WNEajEkaK",
        "scope": "read write groups",
        "token_type": "Bearer"
    }

   - Use the `access_token` from the above response to pass as bearer authorization for the /users, /users/id and /groups services.

    $ http -v localhost:8000/users/ Authorization:"Bearer <access_token>"
    $ http -v localhost:8000/groups/ Authorization:"Bearer <access_token>"
    $ http -v localhost:8000/users/1/ Authorization:"Bearer <access_token>"
    
    $ http -v localhost:8000/api/postings/ Authorization:"Bearer <access_token>"
    $ http -v localhost:8000/api/postings/1/ Authorization:"Bearer <access_token>"
 
 