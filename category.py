import mysql.connector as mariadb
from mysql.connector import Error

from tkinter import *    
from tkinter import messagebox

dbConnect = mariadb.connect(user ="python", password='dbconnector',host ='localhost',port ='3306', database="tasksApp")
dbCursor = dbConnect.cursor()

user = "sample"         #temporary user

def viewOneCategory(id):
    if id > 0:
        b_editCategory = Button(root, text='Edit Category', font=('Arial Narrow Bold', 12), bg='#F46C3E', command=pop_editCategory)
        b_editCategory.place(x=530, y=160)

        b_delCategory = Button(root, text='Delete Category', font=('Arial Narrow Bold', 12), bg='#F46C3E', command=pop_deleteCategory)
        b_delCategory.place(x=640, y=160)
        
    try:
        viewOneCat = "SELECT categoryname, COALESCE(unfinishedtasks,0) FROM category WHERE userid = %s and categoryid = %s;"

        dbCursor.execute(viewOneCat, (user,id,))
        result = dbCursor.fetchone()

        name.config(text=result[0])

        #unfinished = Label(root, text='Unfinished Tasks: ' + str(result[1]), font=('Arial Narrow', 12), fg='white', bg='#3D4448').place(x=800, y=300)
        unfinished.config(text='Unfinished Tasks: ' + str(result[1]))

        print("\n------- One Category -------")
        print("Category Name:", result[0])
        print("Unfinished Tasks:", result[1], "\n")

    except Error as e:
        print("View Category Error: {}".format(e))


def viewAllCategories():
    try:
        viewCat = "SELECT categoryid, categoryname FROM category WHERE userid = %s;"
        
        dbCursor.execute(viewCat, (user,))
        categories = dbCursor.fetchall()

        i = 250
        for row in categories:
            #Radiobutton(root, text=row[1], variable=rb, value=row[0], command=lambda: viewOneCategory(rb.get()), font=('Arial Narrow Bold', 15), fg='white', bg='#292C2E', selectcolor='#292C2E', activebackground='#292C2E', activeforeground='white', pady=10).place(x=20, y=i)
            global c
            c = Radiobutton(root, variable=rb, command=lambda: viewOneCategory(rb.get()), font=('Arial Narrow Bold', 15), fg='white', bg='#292C2E', selectcolor='#292C2E', activebackground='#292C2E', activeforeground='white', pady=10)
            c.place(x=20, y=i)
            c.config(text=row[1], value=row[0])
            i += 50
        
        #same as above
        # global c
        # dict = {}
        # for row in categories:
        #     dict[row[0]] = row[1]
        
        # for val, cname in dict.items():
        #     #c = Radiobutton(root, variable=rb, command=lambda: viewOneCategory(rb.get()), font=('Arial Narrow Bold', 15), fg='white', bg='#292C2E', selectcolor='#292C2E', activebackground='#292C2E', activeforeground='white', pady=10)
        #     c = Radiobutton(canvas, variable=rb, command=lambda: viewOneCategory(rb.get()), font=('Arial Narrow Bold', 15), fg='white', bg='#292C2E', selectcolor='#292C2E', activebackground='#292C2E', activeforeground='white', pady=10)
        #     c.place(x=20, y=i)
        #     c.config(text=cname, value=val)
        #     i += 50
        
    except Error as e:
        print("View Category Error: {}".format(e))

def addCategory(name):
    try:
        addCat = "INSERT INTO category (userid,categoryname) VALUES('" +user+ "', '" +name+ "');" 

        dbCursor.execute(addCat)
        dbConnect.commit()
        print("Successfully added\n")
        messagebox.showinfo('Category Status', "New Category was successfully added!")
        modal.destroy()         # to remove the add category modal
        viewAllCategories()
    except Error as e:
        print("Add Category Error: {}".format(e))


def pop_addCategory():
    global modal
    modal = Toplevel(root, bg='gray')
    modal.title('Add Category')
    modal.geometry('500x200')

    label_add = Label(modal, text='Category Name:', font=('Arial Narrow Bold', 15))
    label_add.pack(padx=10,pady=20)

    input_add = Entry(modal, font=('Arial Narrow', 12))
    input_add.pack()

    b_done = Button(modal, text='Done', font=('Arial Narrow Bold', 12), command=lambda:addCategory(input_add.get()))
    b_done.pack(pady=20)


def editCategory(name):
    try:
        editCat = "UPDATE category SET categoryname = %s WHERE userid = %s AND categoryid = %s;"
        data = (name, user, rb.get())
        
        dbCursor.execute(editCat, data)
        dbConnect.commit()

        print(">> Category was successfully updated!\n")
        messagebox.showinfo('Category Status', "Category was successfully edited!")
        modal.destroy()         # to remove the add category modal
        viewOneCategory(rb.get())
        viewAllCategories()
        #Radiobutton().config(text=name, value=rb.get())

    except Error as e:
        print("Edit Category Error: {}".format(e))


def pop_editCategory():
    global modal
    modal = Toplevel(root, bg='gray')
    modal.title('Edit Category')
    modal.geometry('500x200')

    label_edit = Label(modal, text='New Category Name:', font=('Arial Narrow Bold', 15))
    label_edit.pack(padx=10,pady=20)

    input_edit = Entry(modal, font=('Arial Narrow', 12))
    input_edit.pack()

    b_done = Button(modal, text='Done', font=('Arial Narrow Bold', 12), command=lambda:editCategory(input_edit.get()))
    b_done.pack(pady=20)

def deleteCategory(ans):
    if (ans == 'yes'):
        try:
            deleteCat = "DELETE FROM category WHERE categoryid = %s;"
            
            dbCursor.execute(deleteCat, (rb.get(),))
            dbConnect.commit()

            print(">> Category was deleted!\n")
            messagebox.showinfo('Category Status', "Category was successfully deleted!")
            modal.destroy()         # to remove the add category modal
            
            #c.destroy()
            viewAllCategories()
            
            rb.set(-1)

        except Error as e:
            print("Delete Category Error: {}".format(e))
    else:
        modal.destroy()


def pop_deleteCategory():
    global modal
    modal = Toplevel(root, bg='gray')
    modal.title('Delete Category')
    modal.geometry('500x200')

    label_edit = Label(modal, text='Are You sure you want to delete this category?', font=('Arial Narrow Bold', 15))
    label_edit.pack(padx=10,pady=20)

    yes = Button(modal, text='Yes', font=('Arial Narrow Bold', 12), command=lambda:deleteCategory('yes'))
    yes.place(x=150, y=100)

    no = Button(modal, text='No', font=('Arial Narrow Bold', 12), command=lambda:deleteCategory('no'))
    no.place(x=350, y=100)


#create window
root = Tk()
root.geometry('1024x768')  # w x h
root.title('Tasks App')
root.config(bg='#3D4448')

# canvas
canvas = Canvas(root, width=300, height=768, bg='#292C2E', highlightthickness=0)
canvas.place(x=0, y=0)

# radio buttons
global rb
rb = IntVar()
rb.set(-1)
Radiobutton(root, text='Default Tasks', variable=rb, value=-1, font=('Arial Narrow Bold', 15), fg='white', bg='#292C2E', selectcolor='#292C2E', activebackground='#292C2E', activeforeground='white', pady=10).place(x=10, y=100)
Radiobutton(root, text='View All Tasks', variable=rb, value=0, font=('Arial Narrow Bold', 15), fg='white', bg='#292C2E', selectcolor='#292C2E', activebackground='#292C2E', activeforeground='white', pady=10).place(x=10, y=150)

# labels
title = Label(root, text='<Title>', font=('Arial Narrow Bold', 45), fg='white', bg='#3D4448')
title.place(x=830, y=10)

l_category = Label(root, text='Categories', font=('Arial Narrow Bold', 18), fg='white', bg='#292C2E')
l_category.place(x=10, y=210)

# category name
name = Label(root, font=('Arial Narrow Italic', 28), fg='white', bg='#3D4448')
name.place(x=320, y=100)

# unfinished tasks label
unfinished = Label(root, font=('Arial Narrow', 14), fg='white', bg='#3D4448')
unfinished.place(x=845, y=168)

# buttons
b_createTask = Button(root, text='Create Task', font=('Arial Narrow Bold', 12), bg='#F46C3E')
b_createTask.place(x=320, y=160)

b_addCategory = Button(root, text='Add Category', font=('Arial Narrow Bold', 12), bg='#F46C3E', command=pop_addCategory)
b_addCategory.place(x=420, y=160)

# b_editCategory = Button(root, text='Edit Category', font=('Arial Narrow Bold', 12), bg='#F46C3E', command=pop_editCategory)
# b_editCategory.place(x=530, y=160)

# b_delCategory = Button(root, text='Delete Category', font=('Arial Narrow Bold', 12), bg='#F46C3E', command=pop_deleteCategory)
# b_delCategory.place(x=640, y=160)

viewAllCategories()

root.mainloop()