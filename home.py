#reference: https://pythonexamples.org/python-tkinter-login-form/

#import everything from tkinter
from email import message
from tkinter import *       
from tkinter import messagebox    
from functools import partial


#import database
#reference: https://www.youtube.com/watch?v=oDR7k66x-AU&t=427s&ab_channel=DiscoverPython
import mysql.connector as mariadb

#create mysql connection and define cursor
dbConnect = mariadb.connect(user ="python", password='dbconnector',host ='localhost',port ='3306')
dbCursor = dbConnect.cursor()

##Use tasksapp
dbCursor.execute("USE tasksapp")


#properties and var init
app_title = "TODO.IT"
title = "WELCOME TO " + app_title
btnHeight = 2
btnwidth =10
fontStyle = ("Helvetica",20,"bold")
bgColor = '#040D2C'
fgColor ='white'
loginColor = '#DAF7A6'
signupColor = '#DE303F'
btnFont = ("Helvetica")
signUpFont = ("Helvetica",15,"bold")

#create main window
root = Tk()
root.geometry('500x500')
root.title(title)
root.configure(bg = bgColor)  

#function for user validation
def loginUserFunc(user,password):
    userName = user.get()
    userPassword = password.get()
    
    #validate if fields are not empty
    if (userName and userPassword):
        sql_stata = 'SELECT userid,userpassword FROM user WHERE userid = %s and userpassword = %s';
        validUser = (userName,userPassword)
        dbCursor.execute(sql_stata,validUser)
        ret = dbCursor.fetchone()
        clear_window()
        if ret is None:
            ##did not match any credentials
            warning("Invalid Login")
        else:
            success()
    #warning message
    else:
        warning("Please input values properly")    
    return

##function for clearing window
def clear_window():
        for widgets in root.winfo_children():
            widgets.destroy()
        return
    
def success():        
    ##modify this to enter main app if success
    clear_window()
    successLabel = Label(root,text="SUCCESS!").place(anchor= CENTER, relx =.5,rely = .2)
    return

##return button
def back():
    clear_window()
    mainWind()
    return

#user sign up validation
def signupUserFunc(fname,mname,lname,userName,email,pass1,pass2):
    #check if fields are complete
    #var assignment
    myFname = fname.get()
    myLname = lname.get()
    myMname = mname.get()
    myUserName = userName.get()
    myEmail = email.get()
    myPass1 = pass1.get()
    myPass2 = pass2.get()
    
    if(myFname and myLname and myMname and myUserName and myEmail and myPass1 and myPass2):
        ##validate if two passwords match
        if(myPass1 == myPass2):
            ##check for duplicate user names
            sql_stata = 'SELECT userid FROM user WHERE userid =%s'
            dbCursor.execute(sql_stata,(myUserName,))
            ret = dbCursor.fetchall()
            if ret == []:
                ##save user
                sql_stata = 'INSERT INTO user (userid,fname,minit,lname,email,userpassword) VALUES (%s,%s,%s,%s,%s,%s)'
                userValues = (myUserName,myFname,myMname,myLname,myEmail,myPass1)
                dbCursor.execute(sql_stata,userValues)
                dbConnect.commit()
                messagebox.showinfo(message = "Successfully added. Please log in to proceed")
                loginFunc()
            else: ##if ret is not empty:
                warning("Duplicate Username")
        else: ##if (myPass1 == myPass2):
            warning("Password mismatch")
    else: ##if incomplte fields
        warning("Please input values properly")
    return
    
#sign up function to define all objects in the screen
def signUpFunc():
    clear_window()    
    #create labels and textboxes:
    #textboxes and labels will have a 0.35 relx difference, each input field and labels will have a rely difference of 0.08
    
    #firstname
    fnameLabel = Label(root,text ="First Name: ",font =signUpFont, bg =bgColor, fg = fgColor).place(anchor= CENTER, relx =0.25,rely = .2)
    fname = StringVar()
    fnameInput = Entry(root,textvariable = fname,font =signUpFont).place(anchor= CENTER, relx =.6,rely = .2)
    
    #middle initial
    mnameLabel = Label(root,text ="Middle Initial: ",font =signUpFont, bg =bgColor, fg = fgColor).place(anchor= CENTER, relx =0.25,rely = .28)
    mname = StringVar()
    mnameInput = Entry(root,textvariable = mname,font =signUpFont).place(anchor= CENTER, relx =.6,rely = .28)
    
    #last name
    lnameLabel = Label(root,text ="Last Name: ",font =signUpFont, bg =bgColor, fg = fgColor).place(anchor= CENTER, relx =0.25,rely = .36)
    lname = StringVar()
    lnameInput = Entry(root,textvariable = lname,font =signUpFont).place(anchor= CENTER, relx =.6,rely = .36)
    
    #last name
    emailLabel = Label(root,text ="Email: ",font =signUpFont, bg =bgColor, fg = fgColor).place(anchor= CENTER, relx =0.25,rely = .44)
    email = StringVar()
    emailInput = Entry(root,textvariable = email,font =signUpFont).place(anchor= CENTER, relx =.6,rely = .44)
    
    #last name
    userNameLabel = Label(root,text ="Username: ",font =signUpFont, bg =bgColor, fg = fgColor).place(anchor= CENTER, relx =0.25,rely = .6)
    userName = StringVar()
    userNameInput = Entry(root,textvariable = userName,font =signUpFont).place(anchor= CENTER, relx =.6,rely = .6)
    
    #pass
    pass1Label = Label(root,text ="Password: ",font =signUpFont, bg =bgColor, fg = fgColor).place(anchor= CENTER, relx =0.25,rely = .68)
    pass1 = StringVar()
    pass1NameInput = Entry(root,textvariable = pass1,show='*',font =signUpFont).place(anchor= CENTER, relx =.6,rely = .68)
    
    #pass confirm
    pass2NameLabel = Label(root,text ="Confirm pass ",font =signUpFont, bg =bgColor, fg = fgColor).place(anchor= CENTER, relx =0.25,rely = .76)
    pass2 = StringVar()
    pass2NameInput = Entry(root,textvariable = pass2,show='*',font =signUpFont).place(anchor= CENTER, relx =.6,rely = .76)
    
    #user verification
    signupUser = partial(signupUserFunc,fname,mname,lname,userName,email,pass1,pass2)
    
    #buttons
    signUpBtn = Button(root,text ="Sign up",command = signupUser,bg = loginColor,fg = "black",font=btnFont,height=btnHeight,width=btnwidth).place(anchor= CENTER, relx =.5,rely = .9)
    backBtn = Button(root,text ="Back",bg = signupColor,fg = fgColor,font=btnFont,height=btnHeight,width=btnwidth, command = back).place(anchor= CENTER, relx =.1,rely = 0.05)
    
  
    return

##login function to define the objects in the screen
def loginFunc():
    clear_window()
    #create labels and input box
    #reference for .place: https://stackoverflow.com/questions/33046790/how-to-horizontally-center-a-widget-using-grid
    #username
    userLabel = Label(root,text ="Username: ",font =fontStyle, bg =bgColor, fg = fgColor).place(anchor= CENTER, relx =.5,rely = .2)
    user = StringVar()
    userInput = Entry(root,textvariable = user,font =fontStyle).place(anchor= CENTER, relx =.5,rely = .3)
    
    #pass
    passLabel = Label(root,text="Password: ",font =fontStyle, bg =bgColor, fg = fgColor).place(anchor= CENTER, relx =.5,rely = .4)
    password = StringVar()
    passEntry = Entry(root,textvariable=password,show='*',font =fontStyle).place(anchor= CENTER, relx =.5,rely = .5)

    #login validation
    loginUser = partial(loginUserFunc,user,password)

    #buttons
    loginBtn = Button(root,text="Login",command=loginUser,font=btnFont,bg = loginColor,fg = 'black',height=btnHeight,width=btnwidth).place(anchor= CENTER, relx =.5,rely = .65)
    backBtn = Button(root,text ="Back",bg = signupColor,fg = fgColor,font=btnFont,height=btnHeight,width=btnwidth, command = back).place(anchor= CENTER, relx =.1,rely = 0.05)
    return


def warning(param):
    text = param
    warningMsg = messagebox.showwarning(message=param)


def mainWind():
    #initialize main window and objects
    clear_window()
    welcomeText = Label(root,text=app_title,font =fontStyle, bg =bgColor, fg = fgColor).place(anchor= CENTER, relx =.5,rely = .3)
    btnLogin = Button(root,text = "Login", command=loginFunc,font=btnFont,bg = loginColor,fg = 'black',height=btnHeight,width=btnwidth).place(anchor= CENTER, relx =.5,rely = .42)
    btnSignup = Button(root,text ="Sign up", command=signUpFunc,bg = signupColor,fg = fgColor,font=btnFont,height=btnHeight,width=btnwidth).place(anchor= CENTER, relx =.5,rely = .55)
    return



##output window in a loop and call main window
mainWind()
root.mainloop()