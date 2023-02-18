# Import libraries
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Graphical Interface
root = Tk()  #This is our window
root.title("Database Application")
root.geometry("600x350")


vh_Id = StringVar()
truck = StringVar()
plateNumber = StringVar()
regExpDate = StringVar()
annualInspectionDate = StringVar()
        
# connect with DataBase.
def connectionDatabase():
    myconnection = sqlite3.connect("Vehicle")
    mycursor = myconnection.cursor()

    try:
        mycursor.execute('''
        CREATE TABLE truck(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TRUCK TEXT NOT NULL,
            PLATE_NUMBER TEXT NOT NULL,
            EXPIRE_DATE TEXT NOT NULL,
            INSPECT_DATE TEXT NOT NULL)
        ''')
        messagebox.showinfo("CONNECTION", "Database created")
    except:
        messagebox.showinfo("CONNECTION", "Succesful connection")

def deleteDatabase():
    myconnection = sqlite3.connect("Vehicle")
    mycursor = myconnection.cursor()
    if messagebox.askyesno(message="Data will be lost, do you want to coninue?", title="WARNING"):
        mycursor.execute("DROP TABLE truck")
    else:
        pass

def leaveApplication():
    value = messagebox.askquestion("Leave,", "Do you want to leave?")
    if value == "yes":
        root.destroy()

def cleanData():
    vh_Id.set("")
    truck.set("")
    plateNumber.set("")
    regExpDate.set("")
    annualInspectionDate.set("")

    ############################# METHODS #####################################

def addData():
    myconnection = sqlite3.connect("Vehicle")
    mycursor = myconnection.cursor()
    try:
        data = truck.get(), plateNumber.get(), regExpDate.get(), annualInspectionDate.get()
        mycursor.execute("INSERT INTO truck VALUES(NULL, ?, ?, ?, ?)", (data))
        myconnection.commit()
    except:
        messagebox.showwarning("WARNING", "Error to create record.")
        pass
    cleanData()
    displayData()

def displayData():
    myconnection = sqlite3.connect("Vehicle")
    mycursor = myconnection.cursor()
    records = tree.get_children()
    for element in records:
        tree.delete(element)
    
    try:
        mycursor.execute("SELECT * FROM truck")
        for row in mycursor:
            tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4]))
    except:
        pass

    ##################### Table (tree object)##################################

# Configure style of Heading in Treeview widget.
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview.Heading", background= "azure2", foreground="grey")

tree = ttk.Treeview(height=10, columns=('#0', '#1', '#2', '#3'))
tree.place(x=0, y=130)

# headings in the table.
tree.column('#0', width=100)
tree.heading('#0', text="ID", anchor=CENTER)
tree.heading('#1', text="TRUCK", anchor=CENTER)
tree.heading('#2', text="PLATE NUMBER", anchor=CENTER)
tree.heading('#3', text="REGISTRATION EXPIRATION DATE", anchor=CENTER)
tree.heading('#4', text="ANNUAL INSPECTION DATE", anchor=CENTER)

def selectWithClick(event):
    item = tree.identify('item', event.x, event.y)
    vh_Id.set(tree.item(item,"text"))
    truck.set(tree.item(item, "values")[0])
    plateNumber.set(tree.item(item, "values")[1])
    regExpDate.set(tree.item(item, "values")[2])
    annualInspectionDate.set(tree.item(item, "values")[3])

tree.bind("<Double-1>", selectWithClick)

def updateData():
    myconnection = sqlite3.connect("Vehicle")
    mycursor = myconnection.cursor()
    try:
        data = truck.get(), plateNumber.get(), regExpDate.get(), annualInspectionDate.get()
        mycursor.execute("UPDATE truck SET TRUCK=?, PLATE_NUMBER=?, EXPIRE_DATE=?, INSPECT_DATE=? WHERE ID ="+vh_Id.get(), (data))
        myconnection.commit()
    except:
        messagebox.showwarning("WARNING", "Error to update record")
        pass
    cleanData()
    displayData()

def deleteData():
    myconnection = sqlite3.connect("Vehicle")
    mycursor = myconnection.cursor()
    try:
        if messagebox.askyesno(message="Do you want to delete record?", title="WARNING"):
            mycursor.execute("DELETE FROM truck WHERE ID="+vh_Id.get())
            myconnection.commit()
    except:
        messagebox.showwarning("WARNING", "Error to delete data")
        pass
    cleanData()
    displayData()

########################## INSERT ELEMENTS, WIDGES ################################

menuBar = Menu(root)
menuBase = Menu(menuBar, tearoff=0)
menuBase.add_command(label="Connect Database", command=connectionDatabase)
menuBase.add_command(label="Delete Database", command=deleteDatabase)
menuBase.add_command(label="Leave", command=leaveApplication)
# link to the menu bar. 
menuBar.add_cascade(label="Start", menu=menuBase)

helpMenu = Menu(menuBar, tearoff=0)
helpMenu.add_command(label="Reset Data", command=cleanData)
# link to the help menu.
menuBar.add_cascade(label="Help", menu=helpMenu)

# Text and Entries
e1 = Entry(root, textvariable=id)

label2 = Label(root, text="Vehicle")
label2.place(x=30, y=10)
e2 = Entry(root, textvariable=truck)
e2.place(x=130, y=10)

label3 = Label(root, text="Plate Number")
label3.place(x=30, y=40)
e3 = Entry(root, textvariable=plateNumber)
e3.place(x=130, y=40)

label4 = Label(root, text="Expiration Date")
label4.place(x=340, y=10)
e4 = Entry(root, textvariable=regExpDate)
e4.place(x=490, y=10)

label5 = Label(root, text="Annual Inspection Date")
label5.place(x=340, y=40)
e5 = Entry(root, textvariable=annualInspectionDate)
e5.place(x=490, y=40)

####################### BUTTONS ##########################
b1 = Button(root, text="CREATE RECORD", highlightbackground='MediumPurple1', command=addData)
b1.place(x=50, y=90)

b2 = Button(root, text="UPDATE RECORD", highlightbackground="MediumPurple1", command=updateData)
b2.place(x=210, y=90)

b3 = Button(root, text="SHOW LIST", highlightbackground="MediumPurple1", command=displayData)
b3.place(x=360, y=90)

b4 = Button(root, text="DELETE RECORD",highlightbackground='MediumPurple1', command=deleteData)
b4.place(x=480, y=90)

# Add menu in the window configuration
root.config(menu=menuBar)

root.mainloop()


