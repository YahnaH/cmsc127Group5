Modifications:

1.Created new dump file, tasksApp, added new users and modified userid to be names, so that they may be used as login credentials

2. Created a new user (for python) and grant all access privilege 

    ##Login as root user:
    ##CREATE USER python IDENTIFIED BY 'dbconnector';
    ##GRANT ALL PRIVILEGES ON tasksApp.* to python;
    ##exit
    ##login as python
    ##check if dbs can be accessed

3. Connect to mysql: https://www.youtube.com/watch?v=mt-5FGkw2zY

Note: no need to install anything for Tk since native naman siya sa python

REFERENCE LIST:
https://pythonguides.com/python-tkinter-multiple-windows-tutorial/

https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/