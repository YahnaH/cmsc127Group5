#reference: https://pythonexamples.org/python-tkinter-login-form/

#import everything from tkinter
from tkinter import *       
from functools import partial

#function for user validation
def loginUser(user,password):
    print("username: ",user.get())
    print("password: ",password.get())
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

