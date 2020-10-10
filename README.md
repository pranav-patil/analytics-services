# Analytics Services

Analytics services use the powerful libraries in Python such as Pandas and scikit-learn to analyze the data. The services are developed using the Django Rest Framework is widely used Rest API platform in Python. It also provides in-built authentication, serialization, ORM and web browsable API view. The project demonstrates data analysis and machine learning capabilities.

[Django Framework](https://www.playframework.com/documentation/2.8.x/Home) is a lightweight, stateless and highly scalable web application framework with minimal resource consumption. Play is built on top of Akka and Akka HTTP which enables to develop lightning-fast applications. Although Play is based on MVC programming model, it also offers tools to create fully-featured REST APIs as well as plugins to support important features such as authorization, integration with databases. The Play Services demonstrates the capabilities of Play framework in developing REST services with [OAuth2 Security](https://github.com/nulab/play2-oauth2-provider), [Slick Database Framework](https://www.playframework.com/documentation/2.8.x/PlaySlick), [ReactiveMongo](http://reactivemongo.org/) and external [WebServices](https://www.playframework.com/documentation/2.8.x/ScalaWS).


### Installation and Running of MySQL Server

* Download latest [MySQL Installer](https://dev.mysql.com/downloads/installer/) and follow windows installation steps.
* Alternatively, can download [Latest MySQL Community Server](https://dev.mysql.com/downloads/mysql/) or [MySQL Archive Release](https://downloads.mysql.com/archives/community/) and extract the zip file. MYSQL_HOME is the path to the unzipped MySQL **mysql** directory. Set MYSQL_HOME as an environment (system) variable.
* Create a **my.cnf** file in MYSQL_HOME directory and add below contents. Create **data** and **temp** directories in MYSQL_HOME.

        [client]
        port=3306
        socket=%MYSQL_HOME%\\temp\\mysql.sock

        [mysqld]
        port=3306

        # set basedir to your installation path
        basedir=%MYSQL_HOME%

        # set datadir to the location of your data directory
        datadir=%MYSQL_HOME%\\data

        socket=%MYSQL_HOME%\\temp\\mysql.sock
        key_buffer_size=16M
        max_allowed_packet=128M

        [mysqldump]
        quick

* Initialize MySQL using the below initialize option in mysqld command. Then start the mysqld server.

        $ cd /d %MYSQL_HOME%
        $ bin\mysqld --console --initialize
        $ bin\mysqld --console

* To run MySQL on Windows as a service execute the commands in [Starting MySQL as a Windows Service](https://dev.mysql.com/doc/refman/8.0/en/windows-start-service.html).
* To update root password follow the below commands. The current root password can be found from the output of the previous **mysqld --console --initialize** command, from the line **[Server] A temporary password is generated for root@localhost: xxxxxxxx**.

        $ .\bin\mysql -u root -p xxxxxxxx

        mysql> FLUSH PRIVILEGES;
        mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';

* Create a new database named **playDB**. Then create a new user named **appuser** and grant the permissions to playDB using below **mysql** commands. The user and password are added in **conf/application.conf** configuration file as **slick.dbs.default.db.user** and **slick.dbs.default.db.password**. The FLUSH PRIVILEGES allows to save the changes and reload updated privileges.


        $ bin\mysqld --console

        mysql> CREATE DATABASE playDB;
        mysql> CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'password';
        mysql> GRANT ALL PRIVILEGES ON playDB.* TO 'appuser'@'localhost';
        mysql> FLUSH PRIVILEGES;

* MySQL runs on default port 3306 which can be changed using **my.cnf** configuration file.


### Installation and Running of MongoDB

* Download latest [Windows MongoDB release](https://www.mongodb.org/dl/win32/x86_64-2008plus-ssl) and extract the zip file.
* Create directories **data** and **logs** in MONGODB_HOME directory, were MONGODB_HOME is the path to the unzipped mongodb directory.
* Create file **mongo.log** in MONGODB_HOME/logs directory.
* Create **mongod.cfg** file using [MongoDB configuration options](https://docs.mongodb.com/v3.2/reference/configuration-options/) in MONGODB_HOME/bin directory or copy below mongo configuration in the **mongod.cfg** configuration file.

        systemLog:
          destination: file
          path: MONGODB_HOME/logs
          logAppend: true
        storage:
          dbPath: MONGODB_HOME/data
          journal:
             enabled: true
        net:
          bindIp: 127.0.0.1
          port: 27017

* Go to MONGODB_HOME\bin directory and execute the command "mongod --config mongod.cfg" to run mongodb.
* MongoDB runs on default port 27017.


### Running Django Services

Below are the instructions to download/setup SBT and to run Play Services using command line. Alternatively, [Scala plugin](https://plugins.jetbrains.com/plugin/1347-scala) can be [setup on IntelliJ](https://docs.scala-lang.org/getting-started/intellij-track/getting-started-with-scala-in-intellij.html), running the Play Services using IntelliJ.

* Download the latest [Python3 Release](https://www.python.org/downloads/) and install it. It is recommended to use installer rather than standalone version for windows machine.
* Add `SBT_HOME\bin` directory to System Path.
* Run the below commands in project directory to build and run the Play Services.


        $ pip install poetry
        $ poetry install
        $ poetry run django-admin startproject django-services
        $ poetry run django-admin startapp api
        $ poetry run python manage.py makemigrations
        $ poetry run python manage.py migrate
        $ poetry run python manage.py runserver


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
 
 