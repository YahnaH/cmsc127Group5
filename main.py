from cgitb import text
from select import select
from unicodedata import category
import mysql.connector as mariadb
from mysql.connector import Error

from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

dbConnect = mariadb.connect(user="python", password='dbconnector',
                            host='localhost', port='3306', database="tasksApp")
dbCursor = dbConnect.cursor()

user = "sample"  # temporary user


def viewOneCategory(id):
    global category_id
    if id > 0:
        b_editCategory.place(x=530, y=160)
        b_delCategory.place(x=640, y=160)

        try:
            viewOneCat = "SELECT categoryname, COALESCE(unfinishedtasks,0) FROM category WHERE userid = %s and categoryid = %s;"
            viewUnfinished = "SELECT COUNT(isdone) FROM task WHERE userid = %s AND categoryid = %s AND isdone = 0 GROUP BY categoryid;"
            viewTasksFromCat = "SELECT taskid, title, details, deadlinedate, deadlinetime FROM task WHERE userid = %s and categoryid = %s;"

            dbCursor.execute(viewOneCat, (user, id,))
            result = dbCursor.fetchone()

            print(result[0])

            # stores all tasks in category to records
            dbCursor.execute(viewTasksFromCat, (user, id,))
            cat_Records = dbCursor.fetchall()

            # gets all tasks with isdone = 0, meaning unfinished
            dbCursor.execute(viewUnfinished, (user, id,))
            unfinishedTasks = dbCursor.fetchone()

            update_taskView(cat_Records)

            name.config(text=result[0])
            unfinished.config(text='Unfinished Tasks: ' +
                              str(unfinishedTasks[0]))
            category_id = id

        except Error as e:
            print("View Category Error: {}".format(e))
    else:
        name.config(text='   ')
        unfinished.config(text='   ')
        b_editCategory.place_forget()
        b_delCategory.place_forget()


def getId(cName):
    id = [k for k, v in catDict.items() if v == cName][0]

    global category_id
    category_id = id

    if rb.get() == 0:
        viewOneCategory(id)


def viewAllCategories():
    try:
        viewCat = "SELECT categoryid, categoryname FROM category WHERE userid = %s;"

        dbCursor.execute(viewCat, (user,))
        categories = dbCursor.fetchall()

        global catDict
        for row in categories:
            catDict[row[0]] = row[1]

        category_list = list(catDict.values())

        menu = OptionMenu(root, clicked, *category_list,
                          command=lambda x: getId(x))

        menu.place(x=43, y=255)
        # for the style of selected option from the dropdown menu
        menu.config(font=('Arial Narrow Bold', 14), fg='white',
                    bg='#303335', highlightthickness=0, width=15)
        # for the style of the dropdown menu
        menu['menu'].config(font=('Arial Narrow Bold', 14),
                            fg='white', bg='#555D62')

    except Error as e:
        print("View Category Error: {}".format(e))

    # enable/disable the dropdown menu
    if rb.get() == 0:
        menu.config(state='normal')
    else:
        menu.config(state='disabled')


def addCategory(name):
    if(name == ''):
        messagebox.showinfo('Category Status',
                            "Please enter the category name in the text box.")
    else:
        try:
            addCat = "INSERT INTO category (userid,categoryname) VALUES('" + \
                user + "', '" + name + "');"

            dbCursor.execute(addCat)
            dbConnect.commit()

            messagebox.showinfo('Category Status',
                                "New Category was successfully added!")
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
    label_add = Label(modal, text='Category Name:', font=(
        'Arial Narrow Bold', 15), bg='#292C2E', fg='white')
    label_add.pack(padx=10, pady=20)

    # text box
    input_add = Entry(modal, font=('Arial Narrow', 12))
    input_add.pack()

    # button
    b_done = Button(modal, text='Done', font=('Arial Narrow Bold', 13),
                    bg='#F46C3E', fg='white', command=lambda: addCategory(input_add.get()))
    b_done.pack(side=BOTTOM, pady=30)


def editCategory(name):
    if(name == ''):
        messagebox.showinfo(
            'Category Status', "Please enter the new name for the category in the text box.")
    else:
        try:
            editCat = "UPDATE category SET categoryname = %s WHERE userid = %s AND categoryid = %s;"
            data = (name, user, category_id)

            dbCursor.execute(editCat, data)
            dbConnect.commit()

            messagebox.showinfo('Category Status',
                                "Category was successfully edited!")

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
    label_edit = Label(modal, text='New Category Name:', font=(
        'Arial Narrow Bold', 15), bg='#292C2E', fg='white')
    label_edit.pack(padx=10, pady=20)

    # text box
    input_edit = Entry(modal, font=('Arial Narrow', 12))
    input_edit.pack()

    # button
    b_done = Button(modal, text='Done', font=('Arial Narrow Bold', 13),
                    bg='#F46C3E', fg='white', command=lambda: editCategory(input_edit.get()))
    b_done.pack(side=BOTTOM, pady=30)


def deleteCategory(ans):
    if (ans == 'yes'):
        try:
            deleteCat = "DELETE FROM category WHERE categoryid = %s;"

            dbCursor.execute(deleteCat, (category_id,))
            dbConnect.commit()

            messagebox.showinfo('Category Status',
                                "Category was successfully deleted!")
            modal.destroy()         # to remove the delete category modal

            rb.set(1)
            clicked.set('   ')
            viewOneCategory(0)

            catDict.pop(category_id)
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
    label_edit = Label(modal, text='Are you sure you want to delete this category?', font=(
        'Arial Narrow Bold', 15), bg='#292C2E', fg='white')
    label_edit.pack(padx=10, pady=20)

    # button for yes
    yes = Button(modal, text='Yes', font=('Arial Narrow Bold', 12), bg='#F46C3E',
                 fg='white', width=5, command=lambda: deleteCategory('yes'))
    yes.place(x=150, y=100)

    # button for no
    no = Button(modal, text='No', font=('Arial Narrow Bold', 12), bg='#F46C3E',
                fg='white', width=5, command=lambda: deleteCategory('no'))
    no.place(x=320, y=100)


def options():
    if rb.get() == 1:
        print("Default Tasks")  # insert function call
        viewNoCatTasks()

    elif rb.get() == 2:
        print("View All Tasks")  # insert function call
        viewAllTasks()

    clicked.set('   ')
    viewOneCategory(0)
    viewAllCategories()


def addTask(taskDict):
    if (taskDict["title"] == ''):
        messagebox.showinfo(
            'Task Status', "Please enter a title for the new task in the text box.")
        modal.destroy()
    else:
        try:
            addTsk = "INSERT INTO task (userid,categoryid,title,details,deadlinetime,deadlinedate) VALUES (%s, %s, %s, %s, %s, %s);"

            dbCursor.execute(addTsk, list(taskDict.values()))
            dbConnect.commit()

            messagebox.showinfo('Task Status',
                                "New Task was successfully added!")
            modal.destroy()         # to remove the add category modal

            if (rb.get() == 0):
                viewOneCategory(category_id)
            elif (rb.get() == 1):
                viewNoCatTasks()
            else:
                viewAllTasks()
        except Error as e:
            print("Add Task Error: {}".format(e))


def createNewDict(category, title, details, hours, mins, date):
    tempDetails = details.get()
    tempTime = hours.get() + ":" + mins.get()
    tempDate = date.get()

    if (rb.get() != 1 or rb.get() != 2):
        tempCategory = category
    elif (category.get() == 'None'):
        tempCategory = None
    else:
        tempCategory = [k for k, v in catDict.items() if v ==
                        category.get()][0]

    if (details.get() == ''):
        tempDetails = None

    if (hours.get() == '' or mins.get() == ''):
        tempTime = None

    if (date.get() == ''):
        tempDate = None

    newTask_Dict = {
        "user": user,
        "category": tempCategory,
        "title": title.get(),
        "details": tempDetails,
        "time": tempTime,
        "date": tempDate
    }

    return newTask_Dict


def pop_addTask():
    global category_id
    global modal
    modal = Toplevel(root, bg='#292C2E')
    modal.title('Add Task')
    modal.geometry('500x350')

    # task name label
    addTask_Title = Label(modal, text='Task Name:', font=(
        'Arial Narrow Bold', 15), bg='#292C2E', fg='white')

    # text box
    addTask_Title_Inp = Entry(modal, width=35, font=('Arial Narrow', 12))

    # task detail label
    addTask_Details = Label(modal, text='Task Details:', font=(
        'Arial Narrow Bold', 15), bg='#292C2E', fg='white')

    # text box
    addTask_Det_Inp = Entry(modal, width=35, font=('Arial Narrow', 12))

    # task deadlinetime label
    addTask_Time = Label(modal, text='Task Deadline (Time):', font=(
        'Arial Narrow Bold', 15), bg='#292C2E', fg='white')

    # spin box for hrs
    addTask_Time_Hrs = Spinbox(
        modal, from_=00, to=23, width=3, font=('Arial Narrow Bold', 15))
    addTask_Time_Hrs.delete(0, "end")

    # spin box for min
    addTask_Time_Min = Spinbox(
        modal, from_=00, to=59, width=3, font=('Arial Narrow Bold', 15))
    addTask_Time_Min.delete(0, "end")

    # task deadlineDate label
    addTask_Date = Label(modal, text='Task Deadline (Date):', font=(
        'Arial Narrow Bold', 15), bg='#292C2E', fg='white')

    # text box
    addTask_Date_Inp = DateEntry(modal, width=15, date_pattern='yyyy-mm-dd')
    addTask_Date_Inp.delete(0, "end")

    # if 'Default Tasks' or 'View All Tasks' are selected
    if (rb.get() == 1 or rb.get() == 2):
        addTask_Cat = Label(modal, text='Category:', font=(
            'Arial Narrow Bold', 15), bg='#292C2E', fg='white')
        addTask_Cat.place(x=20, y=30)

        category_list = list(catDict.values())

        addTask_Cat_Inp = OptionMenu(modal, category_id, *category_list)
        addTask_Cat_Inp.place(x=200, y=35)
        addTask_Cat_Inp.config(font=('Arial Narrow Bold', 12),
                               bg='white', highlightthickness=0, width=30)

        # change placements of values
        addTask_Title.place(x=20, y=80)
        addTask_Title_Inp.place(x=200, y=85)
        addTask_Details.place(x=20, y=130)
        addTask_Det_Inp.place(x=200, y=135)
        addTask_Time.place(x=20, y=180)
        addTask_Time_Hrs.place(x=200, y=183)
        addTask_Time_Min.place(x=250, y=183)
        addTask_Date.place(x=20, y=230)
        addTask_Date_Inp.place(x=200, y=235)

    else:
        # change placements of values
        addTask_Title.place(x=20, y=30)
        addTask_Title_Inp.place(x=200, y=35)
        addTask_Details.place(x=20, y=80)
        addTask_Det_Inp.place(x=200, y=85)
        addTask_Time.place(x=20, y=130)
        addTask_Time_Hrs.place(x=200, y=133)
        addTask_Time_Min.place(x=250, y=133)
        addTask_Date.place(x=20, y=180)
        addTask_Date_Inp.place(x=200, y=185)

    b_addTask = Button(modal, text='Done', font=('Arial Narrow Bold', 13),
                       bg='#F46C3E', fg='white', command=lambda: addTask(createNewDict(category_id, addTask_Title_Inp, addTask_Det_Inp, addTask_Time_Hrs, addTask_Time_Min, addTask_Date_Inp)))
    b_addTask.pack(side=BOTTOM, pady=30)


def viewNoCatTasks():
    try:
        viewTask_noCat = "SELECT taskid, title, details, deadlinedate, deadlinetime FROM task WHERE userid = %s AND categoryid IS NULL;"
        dbCursor.execute(viewTask_noCat, (user,))
        noCat_Records = dbCursor.fetchall()

        all_taskList.place_forget()
        default_taskList.place_forget()

        update_taskView(noCat_Records)
    except Error as e:
        print("View Tasks (No Category) Error: {}".format(e))


def viewAllTasks():
    try:
        viewAllTask = "SELECT taskid, categoryname, title, details, deadlinedate, deadlinetime FROM task LEFT JOIN category ON task.categoryid = category.categoryid WHERE task.userid = %s;"
        dbCursor.execute(viewAllTask, (user,))
        allTask_Records = dbCursor.fetchall()

        all_taskList.place_forget()
        default_taskList.place_forget()

        update_taskView(allTask_Records)
    except Error as e:
        print("View All Tasks Error: {}".format(e))


def update_taskView(rec):
    all_taskList.place_forget()
    default_taskList.place_forget()

    if (rb.get() == 2):
        all_taskList.column("Id", stretch=0, width=35)
        all_taskList.column("Category", stretch=0, width=120)
        all_taskList.column("Task Name", stretch=0, width=140)
        all_taskList.column("Details", stretch=0, width=190)
        all_taskList.column("Date", stretch=0, width=100)
        all_taskList.column("Time", stretch=0, width=100)

        for x in allTask_Cols:
            all_taskList.heading(x, text=x)
            all_taskList.grid(row=0, column=0)
            all_taskList.place(x=320, y=220)

        for item in all_taskList.get_children():
            all_taskList.delete(item)

        for row in rec:
            all_taskList.insert('', 'end', values=row)
    else:
        default_taskList.column("Id", stretch=0, width=35)
        default_taskList.column("Task Name", stretch=0, width=190)
        default_taskList.column("Details", stretch=0, width=240)
        default_taskList.column("Date", stretch=0, width=110)
        default_taskList.column("Time", stretch=0, width=110)

        for x in default_Cols:
            default_taskList.heading(x, text=x)
            default_taskList.grid(row=0, column=0)
            default_taskList.place(x=320, y=220)

        for item in default_taskList.get_children():
            default_taskList.delete(item)

        for row in rec:
            default_taskList.insert('', 'end', values=row)


def getrow_default(event):
    rowid = default_taskList.identify_row(event.y)
    item = default_taskList.item(default_taskList.focus())
    t1.set(item['values'][0])  # id
    t2.set(item['values'][1])  # task name
    t3.set(item['values'][2])  # details
    t4.set(item['values'][3])  # date
    t5.set(item['values'][4])  # time


def getrow_all(event):
    rowid = all_taskList.identify_row(event.y)
    item = all_taskList.item(all_taskList.focus())
    t1.set(item['values'][0])  # id
    t2.set(item['values'][1])  # category
    t3.set(item['values'][2])  # task name
    t4.set(item['values'][3])  # details
    t5.set(item['values'][4])  # date
    t6.set(item['values'][5])  # time


# def editTask(dict):
#     try:
#         edit_Task = "UPDATE task SET title = %s, details = %s, deadlinetime = %s, deadlinedate = %s WHERE taskid = %s;"
#         print(dict)
#     except Error as e:
#         print("Edit Task Error: {}".format(e))


# def pop_editTask():
#     global category_id
#     global modal
#     modal = Toplevel(root, bg='#292C2E')
#     modal.title('Add Task')
#     modal.geometry('500x350')

#     # task name label
#     editTask_Title = Label(modal, text='Task Name:', font=(
#         'Arial Narrow Bold', 15), bg='#292C2E', fg='white')

#     # text box
#     editTask_Title_Inp = Entry(modal, width=35, font=(
#         'Arial Narrow', 12), textvariable=t2)

#     # task detail label
#     editTask_Details = Label(modal, text='Task Details:', font=(
#         'Arial Narrow Bold', 15), bg='#292C2E', fg='white')

#     # text box
#     editTask_Det_Inp = Entry(modal, width=35, font=(
#         'Arial Narrow', 12), textvariable=t3)

#     # task deadlinetime label
#     editTask_Time = Label(modal, text='Task Deadline (Time):', font=(
#         'Arial Narrow Bold', 15), bg='#292C2E', fg='white')

#     # spin box for hrs
#     editTask_Time_Hrs = Spinbox(
#         modal, from_=00, to=23, width=3, font=('Arial Narrow Bold', 15), textvariable=t5.get()[0:2])
#     editTask_Time_Hrs.delete(0, "end")

#     # spin box for min
#     editTask_Time_Min = Spinbox(
#         modal, from_=00, to=59, width=3, font=('Arial Narrow Bold', 15), textvariable=t5.get()[3:5])
#     editTask_Time_Min.delete(0, "end")

#     # task deadlineDate label
#     editTask_Date = Label(modal, text='Task Deadline (Date):', font=(
#         'Arial Narrow Bold', 15), bg='#292C2E', fg='white')

#     # text box
#     editTask_Date_Inp = DateEntry(modal, width=15, date_pattern='yyyy-mm-dd')
#     editTask_Date_Inp.delete(0, "end")

#     editTask_Date_Inp.insert(0, t4.get())

#     # if 'Default Tasks' or 'View All Tasks' are selected
#     if (rb.get() == 1 or rb.get() == 2):
#         editTask_Cat = Label(modal, text='Category:', font=(
#             'Arial Narrow Bold', 15), bg='#292C2E', fg='white')
#         editTask_Cat.place(x=20, y=30)

#         category_list = list(catDict.values())

#         editTask_Cat_Inp = OptionMenu(modal, t6, *category_list)
#         editTask_Cat_Inp.place(x=200, y=35)
#         editTask_Cat_Inp.config(font=('Arial Narrow Bold', 12),
#                                 bg='white', highlightthickness=0, width=30)

#         # change placements of values
#         editTask_Title.place(x=20, y=80)
#         editTask_Title_Inp.place(x=200, y=85)
#         editTask_Details.place(x=20, y=130)
#         editTask_Det_Inp.place(x=200, y=135)
#         editTask_Time.place(x=20, y=180)
#         editTask_Time_Hrs.place(x=200, y=183)
#         editTask_Time_Min.place(x=250, y=183)
#         editTask_Date.place(x=20, y=230)
#         editTask_Date_Inp.place(x=200, y=235)

#     else:
#         # change placements of values
#         editTask_Title.place(x=20, y=30)
#         editTask_Title_Inp.place(x=200, y=35)
#         editTask_Details.place(x=20, y=80)
#         editTask_Det_Inp.place(x=200, y=85)
#         editTask_Time.place(x=20, y=130)
#         editTask_Time_Hrs.place(x=200, y=133)
#         editTask_Time_Min.place(x=250, y=133)
#         editTask_Date.place(x=20, y=180)
#         editTask_Date_Inp.place(x=200, y=185)

#     b_editTask = Button(modal, text='Done', font=('Arial Narrow Bold', 13),
#                         bg='#F46C3E', fg='white', command=lambda: editTask(createNewDict(category_id, editTask_Title_Inp, editTask_Det_Inp, editTask_Time_Hrs, editTask_Time_Min, editTask_Date_Inp)))
#     b_editTask.pack(side=BOTTOM, pady=30)


def deleteTask():
    try:
        delete_Task = "DELETE FROM task WHERE taskid = %s;"
        taskVal = int(t1.get())

        if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this task?"):
            dbCursor.execute(delete_Task, (taskVal,))
            dbConnect.commit()
            if (rb.get() == 0):
                viewOneCategory(category_id)
            elif (rb.get() == 1):
                viewNoCatTasks()
            else:
                viewAllTasks()
        else:
            return True
    except Error as e:
        print("Delete Task Error: {}".format(e))


# create window
root = Tk()
root.geometry('1024x768')  # w x h
root.title('Tasks App')
root.config(bg='#3D4448')


# variables
global rb, clicked, category_id, catDict, taskDict, task_id
rb = IntVar()
rb.set(1)
clicked = StringVar()
clicked.set('   ')
category_id = 'None'
catDict = {}
taskDict = {}
t1 = StringVar()
t2 = StringVar()
t3 = StringVar()
t4 = StringVar()
t5 = StringVar()
t6 = StringVar()

# canvas
canvas = Canvas(root, width=300, height=768,
                bg='#292C2E', highlightthickness=0)
canvas.place(x=0, y=0)

# line
canvas.create_line(10, 90, 290, 90, fill='gray')

# radio buttons
Radiobutton(root, text='Default Tasks', variable=rb, value=1, font=('Arial Narrow Bold', 15), fg='white', bg='#292C2E',
            selectcolor='#292C2E', activebackground='#292C2E', activeforeground='white', pady=10, command=options).place(x=10, y=100)
Radiobutton(root, text='All Tasks', variable=rb, value=2, font=('Arial Narrow Bold', 15), fg='white', bg='#292C2E',
            selectcolor='#292C2E', activebackground='#292C2E', activeforeground='white', pady=10, command=options).place(x=10, y=150)
Radiobutton(root, text='Tasks from the Category:', variable=rb, value=0, font=('Arial Narrow Bold', 15), fg='white', bg='#292C2E',
            selectcolor='#292C2E', activebackground='#292C2E', activeforeground='white', pady=10, command=options).place(x=10, y=200)

# emoticon label
emoticon = Label(root, text='^_^', font=(
    'Helvetica', 15), fg='white', bg='#292C2E')
emoticon.place(x=125, y=30)

# title label
title = Label(root, text='ToDo.It', font=(
    'Arial Narrow Bold', 45), fg='#FFC107', bg='#3D4448')
title.place(x=820, y=10)

# category name label
name = Label(root, font=('Arial Narrow Italic', 28), fg='white', bg='#3D4448')
name.place(x=320, y=100)

# unfinished tasks label
unfinished = Label(root, font=('Arial Narrow Bold', 14),
                   fg='white', bg='#3D4448')
unfinished.place(x=845, y=168)

# list of tasks
default_Cols = ("Id", "Task Name", "Details", "Date", "Time")
default_taskList = ttk.Treeview(root, columns=default_Cols,
                                show='headings', height="15")

allTask_Cols = ("Id", "Category", "Task Name", "Details", "Date", "Time")
all_taskList = ttk.Treeview(root, columns=allTask_Cols,
                            show='headings', height="15")

default_taskList.bind('<Double 1>', getrow_default)
all_taskList.bind('<Double 1>', getrow_all)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial Bold', 14), rowheight=30)
style.configure("Treeview", font=('Arial Narrow', 12), rowheight=30)

# buttons
b_createTask = Button(root, text='Create Task', font=(
    'Arial Narrow Bold', 12), bg='#F46C3E', fg='white', command=pop_addTask)
b_createTask.place(x=320, y=160)

b_addCategory = Button(root, text='Add Category', font=(
    'Arial Narrow Bold', 12), bg='#F46C3E', fg='white', command=pop_addCategory)
b_addCategory.place(x=420, y=160)

b_editCategory = Button(root, text='Edit Category', font=(
    'Arial Narrow Bold', 12), bg='#F46C3E', fg='white', command=pop_editCategory)
b_delCategory = Button(root, text='Delete Category', font=(
    'Arial Narrow Bold', 12), bg='#F46C3E', fg='white', command=pop_deleteCategory)

b_exit = Button(root, text='Exit', font=('Arial Narrow Bold', 13),
                bg='#2656D3', fg='white', width=8, command=root.quit)
b_exit.place(x=100, y=710)

# b_editTask = Button(root, text='Edit Task', font=(
#     'Arial Narrow Bold', 13), bg='#F46C3E', fg='white', command=pop_editTask)
# b_editTask.place(x=320, y=710)

b_deleteTask = Button(root, text='Delete Task', font=(
    'Arial Narrow Bold', 13), bg='#F46C3E', fg='white', command=deleteTask)
b_deleteTask.place(x=420, y=710)

viewAllCategories()

root.mainloop()
