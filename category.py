
import mysql.connector as mariadb
from tkinter import *    

from mysql.connector import Error

dbConnect = mariadb.connect(user ="python", password='dbconnector',host ='localhost',port ='3306', database="tasksApp")
dbCursor = dbConnect.cursor()

user = "sample"         #temporary user
categName = input("Category Name: ")

# ADD CATEGORY
try:
    addCat = "INSERT INTO category (userid,categoryname) VALUES('" +user+ "', '" +categName+ "');" 

    dbCursor.execute(addCat)
    dbConnect.commit()
    print("Successfully added\n")

except Error as e:
    print("Add Category Error: {}".format(e))

# VIEW CATEGORY (all categories made by user)
# reference: https://pynative.com/python-mysql-select-query-to-fetch-data/
try:
    viewCat = "SELECT categoryname, COALESCE(unfinishedtasks,0) FROM category WHERE userid = %s;"
    
    dbCursor.execute(viewCat, (user,))
    categories = dbCursor.fetchall()

    print("------- Categories -------")
    for row in categories:
        print("Category Name:", row[0])
        print("Unfinished Tasks:", row[1], "\n")

except Error as e:
    print("View Category Error: {}".format(e))

# VIEW CATEGORY (only one)
try:
    viewOneCat = "SELECT categoryname, COALESCE(unfinishedtasks,0) FROM category WHERE userid = %s and categoryid = %s;"
    idView = input("Category ID to view: ")     #temporary

    dbCursor.execute(viewOneCat, (user,idView,))
    result = dbCursor.fetchone()

    print("\n------- One Category -------")
    print("Category Name:", result[0])
    print("Unfinished Tasks:", result[1], "\n")

except Error as e:
    print("View Category Error: {}".format(e))

# EDIT CATEGORY
try:
    editCat = "UPDATE category SET categoryname = %s WHERE userid = %s AND categoryid = %s;"
    newName = input("New Category Name: ")      #temporary, dapat automatic id from the selected category
    data = (newName, user, 5)           #temporary categoryid
    
    dbCursor.execute(editCat, data)
    dbConnect.commit()

    print(">> Category was successfully updated!\n")

except Error as e:
    print("Edit Category Error: {}".format(e))

# DELETE CATEGORY
try:
    deleteCat = "DELETE FROM category WHERE categoryid = %s;"
    delID = input("Category ID to delete:")      #temporary, dapat automatic id from the selected category
    dataDel = (delID)           #temporary categoryid
    
    dbCursor.execute(deleteCat, (dataDel,))
    dbConnect.commit()

    print(">> Category was deleted!\n")

except Error as e:
    print("Delete Category Error: {}".format(e))

if dbConnect.is_connected():
    dbCursor.close()
    dbConnect.close()
    print("Database connection is closed")


#create window
root = Tk()
root.geometry('1024x768')
root.title('Tasks App')

# insert tkinter codes

root.mainloop()