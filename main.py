# tkinter is a library used to create a standard GUI (Graphical User Interface); object-oriented layer on top of Tcl/Tk
from tkinter import *
# ttk is a module used to style the tkinter widgets
from tkinter import ttk, Tk
# datetime module supplies classes for manipulating dates and times
import datetime
# time module provides carious time-related functions
import time
# tkinter.messagebox module provides a template base class and methods for commonly used configurations
import tkinter.messagebox
# sqlite3 module provides an SQL interface
import sqlite3


# Class creation
class studentsPortal:
    db_name = 'Students.db'

    # Constructor creation
    def __init__(self, root):
        self.root = root
        self.root.title('Students Data Management System')

        # Title creation
        self.label1 = Label(font=('arial', 15, 'bold'), text='School DMS', fg='dark blue')
        self.label1.grid(row=0, column=1)

        # Logo creation
        self.photo = PhotoImage(file='Icon.png')
        self.label = Label(image=self.photo)
        self.label.grid(row=0, column=5)

        # Add a New Record - creation of a table with cells to input data
        frame = LabelFrame(self.root, text='Add a New Record')
        frame.grid(row=1, column=3)

        Label(frame, text='First Name: ').grid(row=1, column=1, sticky=W)
        self.firstname = Entry(frame)
        self.firstname.grid(row=1, column=2)

        Label(frame, text='Last Name: ').grid(row=2, column=1, sticky=W)
        self.lastname = Entry(frame)
        self.lastname.grid(row=2, column=2)

        Label(frame, text='User Name: ').grid(row=3, column=1, sticky=W)
        self.username = Entry(frame)
        self.username.grid(row=3, column=2)

        Label(frame, text='Email Address: ').grid(row=4, column=1, sticky=W)
        self.emailaddress = Entry(frame)
        self.emailaddress.grid(row=4, column=2)

        Label(frame, text='Specialization: ').grid(row=5, column=1, sticky=W)
        self.specialization = Entry(frame)
        self.specialization.grid(row=5, column=2)

        Label(frame, text='Year of Birth: ').grid(row=6, column=1, sticky=W)
        self.yearofbirth = Entry(frame)
        self.yearofbirth.grid(row=6, column=2)

        # Add a New Record - button creation
        ttk.Button(frame, text='Add a New Record', command=self.add).grid(row=7, column=2)

        # Display message after click on a 'Add a New Record' button
        self.message = Label(text='', fg='red')
        self.message.grid(row=8, column=3)

        # Database Table Display Box creation
        self.tree = ttk.Treeview(height=10, columns=['', '', '', '', '', ''])
        self.tree.grid(row=9, column=2, columnspan=3)
        self.tree.heading('#0', text='ID')
        self.tree.column('#0', width=50)
        self.tree.heading('#1', text='First Name')
        self.tree.column('#1', width=90)
        self.tree.heading('#2', text='Last Name')
        self.tree.column('#2', width=90)
        self.tree.heading('#3', text='User Name')
        self.tree.column('#3', width=90)
        self.tree.heading('#4', text='Email Address')
        self.tree.column('#4', width=160)
        self.tree.heading('#5', text='Specialization')
        self.tree.column('#5', width=110)
        self.tree.heading('#6', text='Year of Birth')
        self.tree.column('#6', width=80, stretch=False)

        # Time and Date stamps creation with a function tick()
        def tick():
            d = datetime.datetime.now()
            Today = '{:%d %B %Y}'.format(d)

            t = time.strftime('%I:%M:%S %p')
            self.lblInfo.config(text=(t + '\t' + Today))
            self.lblInfo.after(200, tick)

        self.lblInfo = Label(font=('arial', 14, 'bold'), fg='blue')
        self.lblInfo.grid(row=0, column=2, columnspan=3)
        tick()

        # Menu Bar creation
        chooser = Menu()
        itemone = Menu()

        itemone.add_command(label='Add a New Record', command=self.add)
        itemone.add_command(label='Edit a Record', command=self.edit)
        itemone.add_command(label='Delete a Record', command=self.delete)
        itemone.add_separator()
        itemone.add_command(label='I need help!', command=self.help)
        itemone.add_command(label='Exit a DMS', command=self.exit)

        chooser.add_cascade(label='File', menu=itemone)
        chooser.add_cascade(label='Add a New Record', command=self.add)
        chooser.add_cascade(label='Edit a Record', command=self.edit)
        chooser.add_cascade(label='Delete a Record', command=self.delete)
        chooser.add_cascade(label='I need help!', command=self.help)
        chooser.add_cascade(label='Exit a DMS', command=self.exit)

        root.config(menu=chooser)

        self.view_records()

    # View Database Table with a functions: run_query and view_records
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def view_records(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM Studentslist'
        db_table = self.run_query(query)
        for data in db_table:
            self.tree.insert('', 1000, text=data[0], values=data[1:])

    # Add a New Record - validation function
    def validation(self):
        return len(self.firstname.get()) != 0 and len(self.lastname.get()) != 0 and \
            len(self.username.get()) != 0 and len(self.emailaddress.get()) != 0 and \
            len(self.specialization.get()) != 0 and len(self.yearofbirth.get()) != 0

    # Add a New Record - add_new_record function
    def add_new_record(self):
        if self.validation():
            query = 'INSERT INTO Studentslist VALUES (NULL,?,?,?,?,?,?)'
            parameters = (self.firstname.get(), self.lastname.get(), self.username.get(),
                          self.emailaddress.get(), self.specialization.get(), self.yearofbirth.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Record for {} {} has been added!'.format(self.firstname.get(),
                                                                             self.lastname.get())
            # Clear fields in "Add a New Record" Table
            self.firstname.delete(0, END)
            self.lastname.delete(0, END)
            self.username.delete(0, END)
            self.emailaddress.delete(0, END)
            self.specialization.delete(0, END)
            self.yearofbirth.delete(0, END)

        else:
            self.message['text'] = 'Filling out all fields is mandatory!'

        self.view_records()

    # Add a New Record - add function - messagebox
    def add(self):
        ad = tkinter.messagebox.askquestion('Add a New Record', 'Do you want to add a New Record?')
        if ad == 'yes':
            self.add_new_record()

    # Delete a Record - delete_record function
    def delete_record(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][1]

        except IndexError:
            self.message['text'] = 'Please, select a record that you want to delete.'
            return

        self.message['text'] = ''
        number = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Studentslist WHERE ID = ?'
        self.run_query(query, (number,))
        self.message['text'] = 'Record {} has been deleted!'.format(number)

        self.view_records()

    # Delete a Record - delete function - messagebox
    def delete(self):
        de = tkinter.messagebox.askquestion('Delete a Record', 'Do you want to delete a record?')
        if de == 'yes':
            self.delete_record()

    # Edit a Record - edit_box function
    def edit_box(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]

        except IndexError:
            self.message['text'] = 'Please, select a record to edit it.'
            return

        firstname = self.tree.item(self.tree.selection())['values'][0]
        lastname = self.tree.item(self.tree.selection())['values'][1]
        username = self.tree.item(self.tree.selection())['values'][2]
        emailaddress = self.tree.item(self.tree.selection())['values'][3]
        specialization = self.tree.item(self.tree.selection())['values'][4]
        yearofbirth = self.tree.item(self.tree.selection())['values'][5]

        # Edit a Record - creating a window
        self.edit_root = Toplevel()
        self.edit_root.title('Edit a Record')

        Label(self.edit_root, text='Old First Name').grid(row=0, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=firstname), state='readonly'). \
            grid(row=0, column=2)
        Label(self.edit_root, text='New First Name').grid(row=1, column=1, sticky=W)
        new_firstname = Entry(self.edit_root)
        new_firstname.grid(row=1, column=2)

        Label(self.edit_root, text='Old Last Name').grid(row=2, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=lastname), state='readonly'). \
            grid(row=2, column=2)
        Label(self.edit_root, text='New Last Name').grid(row=3, column=1, sticky=W)
        new_lastname = Entry(self.edit_root)
        new_lastname.grid(row=3, column=2)

        Label(self.edit_root, text='Old User Name').grid(row=4, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=username), state='readonly'). \
            grid(row=4, column=2)
        Label(self.edit_root, text='New User Name').grid(row=5, column=1, sticky=W)
        new_username = Entry(self.edit_root)
        new_username.grid(row=5, column=2)

        Label(self.edit_root, text='Old Email Address').grid(row=6, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=emailaddress), state='readonly'). \
            grid(row=6, column=2)
        Label(self.edit_root, text='New Email Address').grid(row=7, column=1, sticky=W)
        new_emailaddress = Entry(self.edit_root)
        new_emailaddress.grid(row=7, column=2)

        Label(self.edit_root, text='Old Specialization').grid(row=8, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=specialization), state='readonly'). \
            grid(row=8, column=2)
        Label(self.edit_root, text='New Specialization').grid(row=9, column=1, sticky=W)
        new_specialization = Entry(self.edit_root)
        new_specialization.grid(row=9, column=2)

        Label(self.edit_root, text='Old Year Of Birth').grid(row=10, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=yearofbirth), state='readonly'). \
            grid(row=10, column=2)
        Label(self.edit_root, text='New Year Of Birth').grid(row=11, column=1, sticky=W)
        new_yearofbirth = Entry(self.edit_root)
        new_yearofbirth.grid(row=11, column=2)

        # Save changes Button
        Button(self.edit_root, text='Save changes!',
               command=lambda:
               self.edit_record(new_firstname.get(), firstname, new_lastname.get(), lastname, new_username.get(),
                                username, new_emailaddress.get(), emailaddress, new_specialization.get(),
                                specialization, new_yearofbirth.get(), yearofbirth)).grid(row=12, column=2, sticky=W)
        self.edit_root.mainloop()

    # Edit a Record - edit_record function
    def edit_record(self, new_firstname, firstname, new_lastname, lastname, new_username, username,
                    new_emailaddress, emailaddress, new_specialization, specialization, new_yearofbirth, yearofbirth):
        query = 'UPDATE Studentslist SET FirstName=?, LastName=?, UserName=?, EmailAddress=?, ' \
                'Specialization=?, YearOfBirth=? WHERE FirstName=? AND LastName=? AND UserName=? AND EmailAddress=? AND ' \
                'Specialization=? AND YearOfBirth=?'
        parameters = (new_firstname, new_lastname, new_username, new_emailaddress, new_specialization, new_yearofbirth,
                      firstname, lastname, username, emailaddress, specialization, yearofbirth)
        self.run_query(query, parameters)
        self.edit_root.destroy()
        self.message['text'] = '{} details have been changed to {}'.format(firstname, new_firstname)
        self.view_records()

    # Edit a Record - edit function - messagebox
    def edit(self):
        ed = tkinter.messagebox.askquestion('Edit a record', 'Do you want to edit a record?')
        if ed == 'yes':
            self.edit_box()

    # Help - help function - messagebox
    def help(self):
        tkinter.messagebox.showinfo('Log', 'Report has been sent!')

    # Exit - exit function - messagebox
    def exit(self):
        ex = tkinter.messagebox.askquestion('Exit Application', 'Do you want to close your application?')
        if ex == 'yes':
            root.destroy()


if __name__ == '__main__':
    root = Tk()
    root.geometry('900x500+400+100')
    application = studentsPortal(root)

# root.mainloop() is a method in the main window which we execute when we want to run our application
root.mainloop()
