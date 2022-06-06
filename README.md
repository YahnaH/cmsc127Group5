CMSC 127 - Group 5

Yanna Denise A. Hilario
MattheW Jason Lucero
Reinalyn Madrid


If you will be using this app (provided you already downloaded the source code):

1.Download the dump file for the taskapp.sql

2. Login as root user

3. Created a new user (for python) and grant all access privilege 

    ##Login as root user:
    ##CREATE USER python IDENTIFIED BY 'dbconnector';
    ##GRANT ALL PRIVILEGES ON tasksApp.* to python;
    ##exit
    ##login as python
    ##check if dbs can be accessed

4.Connect python to mysql
    (a.) You can watch this link to guide you step by step on how to install the db connector
        Connect to mysql: https://www.youtube.com/watch?v=mt-5FGkw2zY

    (b.) or you can try running 'pip install mysql-connector-python' on VScode terminal


Note: no need to install anything for Tk since it is native in python

To edit a task:
- Double click the task/row first, then click the edit task button.

To delete a task:
- Double click the task/row first, then click the delete task button.

To check or uncheck the box:
- Click the task/row first, then right-click the checkbox.

REFERENCE LIST:
https://pythonguides.com/python-tkinter-multiple-windows-tutorial/

https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
