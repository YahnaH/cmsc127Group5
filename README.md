Modifications:

1.Created new dump file, tasksApp, added new users and modified userid to be names, so that they may be used as login credentials

2. Created a new user (for python) and grant all access privilege 

    ##Login as root user:
    ##CREATE USER python IDENTIFIED BY 'dbconnector';
    ##GRANT ALL PRIVILEGES ON tasksApp.* to python;
    ##exit
    ##login as python
    ##check if dbs can be accessed