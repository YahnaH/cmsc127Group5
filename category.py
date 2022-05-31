import mysql.connector as mariadb
from mysql.connector import Error

from tkinter import *    
from tkinter import messagebox

dbConnect = mariadb.connect(user ="python", password='dbconnector',host ='localhost',port ='3306', database="tasksApp")
dbCursor = dbConnect.cursor()

user = "sample"         #temporary user

def viewOneCategory(id):
    if id > 0:
        b_editCategory.place(x=530, y=160)
        b_delCategory.place(x=640, y=160)
        
        try:
            viewOneCat = "SELECT categoryname, COALESCE(unfinishedtasks,0) FROM category WHERE userid = %s and categoryid = %s;"

            dbCursor.execute(viewOneCat, (user,id,))
            result = dbCursor.fetchone()

            name.config(text=result[0])
            unfinished.config(text='Unfinished Tasks: ' + str(result[1]))

        except Error as e:
            print("View Category Error: {}".format(e))
    else:
        name.config(text='   ')
        unfinished.config(text='   ')
        b_editCategory.place_forget()
        b_delCategory.place_forget()

def getId(cName):
    id = [k for k, v in dict.items() if v == cName][0]
    
    global category_id
    category_id = id

    if rb.get()==0:
        viewOneCategory(id)


def viewAllCategories():
    try:
        viewCat = "SELECT categoryid, categoryname FROM category WHERE userid = %s;"
        
        dbCursor.execute(viewCat, (user,))
        categories = dbCursor.fetchall()
        
        global dict
        for row in categories:
            dict[row[0]] = row[1]
        
        category_list = list(dict.values())

        menu = OptionMenu(root, clicked, *category_list, command=lambda x:getId(x))
        
        menu.place(x=43, y=255)
        menu.config(font=('Arial Narrow Bold', 14), fg='white', bg='#303335', highlightthickness=0, width=15)       #for the style of selected option from the dropdown menu
        menu['menu'].config(font=('Arial Narrow Bold', 14), fg='white',bg='#555D62')        #for the style of the dropdown menu
        
    except Error as e:
        print("View Category Error: {}".format(e))
    
    # enable/disable the dropdown menu
    if rb.get() == 0:
        menu.config(state='normal')
    else:
        menu.config(state='disabled')

def addCategory(name):
    if(name == ''):
        messagebox.showinfo('Category Status', "Please enter the category name in the text box.")
    else:
        try:
            addCat = "INSERT INTO category (userid,categoryname) VALUES('" +user+ "', '" +name+ "');" 

            dbCursor.execute(addCat)
            dbConnect.commit()

            messagebox.showinfo('Category Status', "New Category was successfully added!")
            modal.destroy()         # to remove the add category modal
            viewAllCategories()
        except Error as e:
            print("Add Category Error: {}".format(e))


def pop_addCategory():
    # modal window
    global modal
    modal = Toplevel(root, bg='#292C2E')
    modal.title('Add Category')
    modal.geometry('500x200')

    # category name label
    label_add = Label(modal, text='Category Name:', font=('Arial Narrow Bold', 15), bg='#292C2E', fg='white')
    label_add.pack(padx=10,pady=20)

    # text box
    input_add = Entry(modal, font=('Arial Narrow', 12))
    input_add.pack()

    # button
    b_done = Button(modal, text='Done', font=('Arial Narrow Bold', 13), bg='#F46C3E', fg='white', command=lambda:addCategory(input_add.get()))
    b_done.pack(side=BOTTOM,pady=30)


def editCategory(name):
    if(name == ''):
        messagebox.showinfo('Category Status', "Please enter the new name for the category in the text box.")
    else:
        try:
            editCat = "UPDATE category SET categoryname = %s WHERE userid = %s AND categoryid = %s;"
            data = (name, user, category_id)

            dbCursor.execute(editCat, data)
            dbConnect.commit()

            messagebox.showinfo('Category Status', "Category was successfully edited!")
            
            modal.destroy()         # to remove the edit category modal
            viewOneCategory(category_id)
            viewAllCategories()
            clicked.set(name)

        except Error as e:
            print("Edit Category Error: {}".format(e))


def pop_editCategory():
    # modal window
    global modal
    modal = Toplevel(root, bg='#292C2E')
    modal.title('Edit Category')
    modal.geometry('500x200')

    # new category name label
    label_edit = Label(modal, text='New Category Name:', font=('Arial Narrow Bold', 15), bg='#292C2E', fg='white')
    label_edit.pack(padx=10,pady=20)

    # text box
    input_edit = Entry(modal, font=('Arial Narrow', 12))
    input_edit.pack()

    # button
    b_done = Button(modal, text='Done', font=('Arial Narrow Bold', 13), bg='#F46C3E', fg='white', command=lambda:editCategory(input_edit.get()))
    b_done.pack(side=BOTTOM,pady=30)


def deleteCategory(ans):
    if (ans == 'yes'):
        try:
            deleteCat = "DELETE FROM category WHERE categoryid = %s;"
            
            dbCursor.execute(deleteCat, (category_id,))
            dbConnect.commit()

            messagebox.showinfo('Category Status', "Category was successfully deleted!")
            modal.destroy()         # to remove the delete category modal
            
            rb.set(1)
            clicked.set('   ')
            viewOneCategory(0)

            dict.pop(category_id)
            viewAllCategories()

        except Error as e:
            print("Delete Category Error: {}".format(e))
    else:
        modal.destroy()


def pop_deleteCategory():
    # modal window
    global modal
    modal = Toplevel(root, bg='#292C2E')
    modal.title('Delete Category')
    modal.geometry('500x200')

    # label
    label_edit = Label(modal, text='Are you sure you want to delete this category?', font=('Arial Narrow Bold', 15),bg='#292C2E', fg='white')
    label_edit.pack(padx=10,pady=20)

    # button for yes
    yes = Button(modal, text='Yes', font=('Arial Narrow Bold', 12), bg='#F46C3E', fg='white', width=5, command=lambda:deleteCategory('yes'))
    yes.place(x=150, y=100)

    # button for no
    no = Button(modal, text='No', font=('Arial Narrow Bold', 12), bg='#F46C3E', fg='white', width=5, command=lambda:deleteCategory('no'))
    no.place(x=320, y=100)

def options():
    if rb.get() == 1:
        print("Default Tasks")     #insert function call
    elif rb.get() == 2:
        print("View All Tasks")     #insert function call
    
    clicked.set('   ')
    viewOneCategory(0)
    viewAllCategories()

#create window
root = Tk()
root.geometry('1024x768')  # w x h
root.title('Tasks App')
root.config(bg='#3D4448')

# variables
global rb, clicked, category_id, dict
rb = IntVar()
rb.set(1)
clicked = StringVar()
clicked.set('   ')
dict = {}

# canvas
canvas = Canvas(root, width=300, height=768, bg='#292C2E', highlightthickness=0)
canvas.place(x=0, y=0)

# line
canvas.create_line(10,90,290,90, fill='gray')

# radio buttons
Radiobutton(root, text='Default Tasks', variable=rb, value=1, font=('Arial Narrow Bold', 15), fg='white', bg='#292C2E', selectcolor='#292C2E', activebackground='#292C2E', activeforeground='white', pady=10, command=options).place(x=10, y=100)
Radiobutton(root, text='All Tasks', variable=rb, value=2, font=('Arial Narrow Bold', 15), fg='white', bg='#292C2E', selectcolor='#292C2E', activebackground='#292C2E', activeforeground='white', pady=10, command=options).place(x=10, y=150)
Radiobutton(root, text='Tasks from the Category:', variable=rb, value=0, font=('Arial Narrow Bold', 15), fg='white', bg='#292C2E', selectcolor='#292C2E', activebackground='#292C2E', activeforeground='white', pady=10, command=options).place(x=10, y=200)

#emoticon label
emoticon = Label(root, text='^_^', font=('Helvetica', 15), fg='white', bg='#292C2E')
emoticon.place(x=125, y=30)

# title label
title = Label(root, text='ToDo.It', font=('Arial Narrow Bold', 45), fg='#FFC107', bg='#3D4448')
title.place(x=820, y=10)

# category name label
name = Label(root, font=('Arial Narrow Italic', 28), fg='white', bg='#3D4448')
name.place(x=320, y=100)

# unfinished tasks label
unfinished = Label(root, font=('Arial Narrow Bold', 14), fg='white', bg='#3D4448')
unfinished.place(x=845, y=168)

# buttons
b_createTask = Button(root, text='Create Task', font=('Arial Narrow Bold', 12), bg='#F46C3E', fg='white')
b_createTask.place(x=320, y=160)

b_addCategory = Button(root, text='Add Category', font=('Arial Narrow Bold', 12), bg='#F46C3E', fg='white', command=pop_addCategory)
b_addCategory.place(x=420, y=160)

b_editCategory = Button(root, text='Edit Category', font=('Arial Narrow Bold', 12), bg='#F46C3E', fg='white', command=pop_editCategory)
b_delCategory = Button(root, text='Delete Category', font=('Arial Narrow Bold', 12), bg='#F46C3E', fg='white', command=pop_deleteCategory)

b_exit = Button(root, text='Exit', font=('Arial Narrow Bold', 13), bg='#2656D3', fg='white', width=8, command=root.quit)
b_exit.place(x=100, y=710)

viewAllCategories()

root.mainloop()