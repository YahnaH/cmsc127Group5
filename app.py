#reference: https://pythonexamples.org/python-tkinter-login-form/

#import everything from tkinter
from tkinter import *       
from functools import partial

#import database
#reference: https://www.youtube.com/watch?v=oDR7k66x-AU&t=427s&ab_channel=DiscoverPython
import mysql.connector as mariadb

#create mysql connection and define cursor
dbConnect = mariadb.connect(user ="python", password='dbconnector',host ='localhost',port ='3306')
dbCursor = dbConnect.cursor()

##SHOW DBS and use tasksapp
dbCursor.execute("SHOW DATABASES")
for x in dbCursor:
    print(x)

dbCursor.execute("USE tasksapp")

#function for user validation
def loginUser(user,password):
    userName = user.get()
    userPassword = password.get()
    sql_stata = 'SELECT userid,userpassword FROM user WHERE userid = %s and userpassword = %s';
    validUser = (userName,userPassword)
    dbCursor.execute(sql_stata,validUser)
    res = dbCursor.fetchone()
    clear_window()
    if res is None:
        ##did not match any credentials
        success(0)
    else:
        success(1)
    return

##function for clearing window
def clear_window():
        for widgets in root.winfo_children():
            widgets.destroy()
        return
    
def success(params):
    if params == 1:
        successLabel = Label(root,text="SUCCESS!").place(anchor= CENTER, relx =.5,rely = .2)
    else:
        successLabel = Label(root,text="FAILED!").place(anchor= CENTER, relx =.5,rely = .2)
    return

#create window
root = Tk()
root.geometry('400x150')
root.title('User Login')

#create labels and input box
#reference for .place: https://stackoverflow.com/questions/33046790/how-to-horizontally-center-a-widget-using-grid
userLabel = Label(root,text ="Username: ").place(anchor= CENTER, relx =.5,rely = .2)
user = StringVar()
userInput = Entry(root,textvariable = user).place(anchor= CENTER, relx =.5,rely = .3)
passLabel = Label(root,text="Password: ").place(anchor= CENTER, relx =.5,rely = .5)
password = StringVar()
passEntry = Entry(root,textvariable=password,show='*').place(anchor= CENTER, relx =.5,rely = .6)

loginUser = partial(loginUser,user,password)

loginBtn = Button(root,text="Login",command=loginUser).place(anchor= CENTER, relx =.5,rely = .8)

##output window in a loop
root.mainloop()

