from tkinter import *                           # Imports all classes, functions, and variables from the tkinter module
from PIL import Image,ImageTk                   # Imports the Image and ImageTk modules from the Python Imaging Library (PIL)
from tkinter import ttk                         # Import themed tkinter widgets
from tkinter import messagebox                  # Import messagebox for displaying message boxes
import sqlite3                                  # Imports the sqlite3 module, which is used for working with SQLite databases in Python

class EnrollmentClass:
    def __init__(self, root):
        self.root = root                                                    # Initializes the root window
        self.root.title("Inscrições - Sistema de Gestão de Resultados")     # Title of the window
        self.root.geometry("1290x480")                                      # Dimensions of the window
        self.root.config(bg="white")                                        # Background color of the window
        self.root.focus_force()                                             # Forces the focus on the window
        self.root.resizable(False, False)
        
        # =============== Title ===============
        # Creates a label for the title and places it at the top of the window
        title = Label(self.root, 
                        text="Gerenciar Inscrições", 
                        font=("goudy old style",20,"bold"), 
                        bg="#033054", 
                        fg="white"
                    )
        title.place(x=10, y=15, width=1270, height=35)

        # =============== Variables ===============
        # Initialize the variables
        self.var_enr_id = StringVar()
        self.var_roll = StringVar()
        self.var_student_name = StringVar()
        self.var_cid = StringVar()
        self.var_course_name = StringVar()
        self.var_course_description = StringVar()
        self.roll_list = []                                                 # List to store roll numbers
        self.course_list = []                                               # List to store course numbers
        self.fetch_student()
        self.fetch_course()

        # =============== Labels ===============
        # Creates and places the label for the 'Select Students' field
        lbl_select = Label(self.root, text="Estudante", font=("goudy old style", 15, "bold"), bg="white")
        lbl_select.place(x=50, y=70)
        # Creates and places the label for the 'Student Name' field
        lbl_student_name = Label(self.root, text="Nome", font=("goudy old style", 15, "bold"), bg="white")
        lbl_student_name.place(x=50, y=110)
        # Creates and places the label for the 'Select Course' field
        lbl_course = Label(self.root, text="Curso", font=("goudy old style", 15, "bold"), bg="white")
        lbl_course.place(x=50, y=150)
        # Creates and places the label for the 'Course Name' field
        lbl_course_name = Label(self.root, text="Descrição", font=("goudy old style", 15, "bold"), bg="white")
        lbl_course_name.place(x=50, y=190)

        # =============== Entry Fields ===============
        # Combobox for selecting a student
        self.txt_student = ttk.Combobox(self.root, textvariable=self.var_roll, values=self.roll_list, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_student.place(x=210, y=70, width=200)
        self.txt_student.set("Select")
        self.txt_student.bind("<<ComboboxSelected>>", self.on_student_selected)
        # Creates and places the entry fields for the student name
        txt_name = Entry(self.root, textvariable=self.var_student_name, font=("goudy old style", 15, "bold"), bg="lightyellow", state="readonly")
        txt_name.place(x=210, y=110, width=200)

        # Combobox for selecting a course
        self.txt_course = ttk.Combobox(self.root, textvariable=self.var_course_name, values=self.course_list, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_course.place(x=210, y=150, width=200)
        self.txt_course.set("Select")
        self.txt_course.bind("<<ComboboxSelected>>", self.on_course_selected)
        # Creates the entry field for the course description
        self.course_txt_description = Text(self.root, font=("goudy old style", 15, "bold"), bg="lightyellow", state="disabled")
        self.course_txt_description.place(x=210, y=190, width=400, height=200)


        # =============== Buttons ===============
        # Create and place the button to call the 'Submit' function (def add)
        self.btn_add = Button(self.root, text="Salvar", font=("times new roman", 15), bg="#2196f3", fg="white", cursor="hand2", command=self.add)
        self.btn_add.place(x=210, y=420, width=120, height=35)
        # Create and place the button to call the 'Delete' function (def delete)
        self.btn_clear = Button(self.root, text="Deletar", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete)
        self.btn_clear.place(x=350, y=420, width=120, height=35)
        # Create and place the button to call the 'Clear' function (def clear)
        self.btn_clear = Button(self.root, text="Limpar", font=("times new roman", 15), bg="#607d8b", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=490, y=420, width=120, height=35)


        # =============== Seach Panel ===============
        self.var_search_course = StringVar()                           # Variable to store the 'search course' query

        # Creates a label for the 'search course'
        lbl_search_courseName = Label(self.root, text="Curso:", font=("Time News Roman", 11), bg="white")
        lbl_search_courseName.place(x=700, y=70)
        # Creates an entry field for the search input
        txt_search_courseName = Entry(self.root, textvariable=self.var_search_course, font=("goudy old style", 11, "bold"), bg="lightyellow")
        txt_search_courseName.place(x=760, y=70, width=110)
        # Creates the search button, which calls the 'search course' method
        self.btn_search = Button(self.root, text="Pesquisar", font=("goudy old style", 13, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.search_enrollment_course)
        self.btn_search.place(x=880, y=70, width=80, height=24)


        self.var_search_student = StringVar()                           # Variable to store the search query

        # Creates a label for the 'search student'
        lbl_search_studentRoll = Label(self.root, text="Estudante:", font=("Time News Roman", 11), bg="white")
        lbl_search_studentRoll.place(x=970, y=70)
        # Creates an entry field for the search input
        txt_search_studentRoll = Entry(self.root, textvariable=self.var_search_student, font=("goudy old style", 11, "bold"), bg="lightyellow")
        txt_search_studentRoll.place(x=1050, y=70, width=100)
        # Creates the search button, which calls the 'search student' method
        self.btn_search = Button(self.root, text="Pesquisar", font=("goudy old style", 13, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.search_enrollment_student)
        self.btn_search.place(x=1160, y=70, width=80, height=24)


        # --------------- Enrollment Table Widget ---------------
        # Creates a frame to hold the 'enrollment table widget'
        self.E_Frame = Frame(self.root,
                                bd=2,
                                relief=RIDGE 
                            )
        self.E_Frame.place(x=702, y=110, width=540, height=345)

        # Creates vertical and horizontal scrollbars for the 'enrollment table widget'
        scroll_y = Scrollbar(self.E_Frame, orient=VERTICAL)
        scroll_x = Scrollbar(self.E_Frame, orient=HORIZONTAL)

        # Creates a 'Treeview' widget for the 'enrollment table widget' with the specified columns
        self.EnrollmentTable = ttk.Treeview(self.E_Frame,
                                            columns=("enr_id", "roll", "student_name", "cid", "course_name", "course_description"),
                                            xscrollcommand=scroll_x.set,
                                            yscrollcommand=scroll_y.set
                                        )
        
        # Packs the scrollbars to the bottom and right sides of the frame
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.EnrollmentTable.xview)                     # Configures the horizontal scrollbar to control the x view of the 'enrollment table widget'
        scroll_y.config(command=self.EnrollmentTable.yview)                     # Configures the vertical scrollbar to control the y view of the 'enrollment table widget'

        # Defines the headings for the 'enrollment table widget' columns
        self.EnrollmentTable.heading("enr_id", text="Inscrição ID")
        self.EnrollmentTable.heading("roll", text="Estudante ID")
        self.EnrollmentTable.heading("student_name", text="Nome do Estudante")
        self.EnrollmentTable.heading("cid", text="Curso ID")
        self.EnrollmentTable.heading("course_name", text="Nome do Curso")
        self.EnrollmentTable.heading("course_description", text="Descrição do Curso")

        # Displays only the headings (no index column)
        self.EnrollmentTable["show"] = 'headings'
        # Sets the width for each column
        self.EnrollmentTable.column("enr_id", width=100)
        self.EnrollmentTable.column("roll", width=100)
        self.EnrollmentTable.column("student_name", width=120)
        self.EnrollmentTable.column("cid", width=100)
        self.EnrollmentTable.column("course_name", width=100)
        self.EnrollmentTable.column("course_description", width=150)

        self.EnrollmentTable.pack(fill=BOTH, expand=1)                          # Packs the 'enrollment table widget' to fill the frame
        self.EnrollmentTable.bind("<ButtonRelease-1>", self.get_data)           # Binds a click event to the 'enrollment table widget' to call the 'get_data' method
        self.show()                                                             # Calls the 'show' method to populate the table with data


    # When a row in the 'enrollment table widget' is clicked, this method is called. It sets the entry fields in the form with the data from the selected row.
    def get_data(self, ev):

        r = self.EnrollmentTable.focus()
        content = self.EnrollmentTable.item(r)                                  # Retrieves the item data for the selected row
        row = content["values"]                                                 # Extracts the values from the item data

        # Sets the form fields with the data from the selected row
        self.var_enr_id.set(row[0]) 
        self.var_roll.set(row[1])
        self.var_student_name.set(row[2])                                      
        self.var_cid.set(row[3])
        self.var_course_name.set(row[4])

        self.course_txt_description.config(state=NORMAL)
        self.course_txt_description.delete('1.0', END)
        self.course_txt_description.insert(END, row[5])
        self.course_txt_description.config(state=DISABLED)


    # This function fetches all the records from the 'enrollment' table in the database and populates the 'enrollment table widget' with this data
    def show(self):
        con = sqlite3.connect(database="rms.db")                                    # Connects to the SQLite database
        cur = con.cursor()                                                          # Creates a cursor object to interact with the database

        try:
            cur.execute("select * from enrollment")                                 # Executes a SQL query to select all records from the 'enrollment' table
            rows = cur.fetchall()                                                   # Fetch all the rows returned by the query
            self.EnrollmentTable.delete(*self.EnrollmentTable.get_children())       # Clears the current content of the course table

            # Loop through the rows
            for row in rows:
                self.EnrollmentTable.insert('', END, values=row)                    # Inserts each row into the 'enrollment table widget'

            # Closes the database connection 
            con.close()
        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")                # Shows an error message if an exception occurs


    def on_student_selected(self, event):
        self.search_student()

    def on_course_selected(self, event):
        self.search_course()

    
    # Adds the roll number from the database to the 'roll_list' variable, which is used by the combobox
    def fetch_student(self):
        con = sqlite3.connect(database="rms.db")                        # Connects to the SQLite database
        cur = con.cursor()                                              # Creates a cursor object to interact with the database

        try:
            # Execute a SQL query to select all 'roll' numbers from the 'student' table
            cur.execute("select roll from student")
            rows = cur.fetchall()                                       # Fetchs all the results of the query

            # Check if any rows are returned
            if (len(rows)>0):
                # Loops through each row in the results
                for row in rows:
                    # Appends the roll number to the roll_list
                    self.roll_list.append(row[0])
        
            # Closes the database connection 
            con.close() 
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    # Adds the roll number from the database to the 'course_list' variable, which is used by the combobox
    def fetch_course(self):
        con = sqlite3.connect(database="rms.db")                        # Connects to the SQLite database
        cur = con.cursor()                                              # Creates a cursor object to interact with the database

        try:
            # Execute a SQL query to select all 'cid' numbers from the student table
            cur.execute("select name from course")
            rows = cur.fetchall()                                       # Fetchs all the results of the query

            # Check if any rows are returned
            if (len(rows)>0):
                # Loops through each row in the results
                for row in rows:
                    # Appends the 'cid' number to the 'course_list'
                    self.course_list.append(row[0])
        
            # Closes the database connection 
            con.close() 
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")
    

    # Searchs in the database for the 'student' where the roll is the same as the variable 'var_roll' and uses its data to fill the 'name' and 'course' variables
    def search_student(self):
        con = sqlite3.connect(database="rms.db")                        # Connects to the SQLite database
        cur = con.cursor()                                              # Creates a cursor object to interact with the database

        try:
            # Executes a SQL query to select the name and course from the student table where the roll matches the input
            cur.execute("select name from student where roll=?", (self.var_roll.get(), ))
            row = cur.fetchone()                                        # Fetchs one result from the query
            
            # Checks if a row is returned
            if(row!=None):
                # Sets the 'name' and 'course' variables with the fetched data
                self.var_student_name.set(row[0])
            else:
                # Displays an error message if no record is found
                messagebox.showerror("Erro", "No record fond", parent=self.root)

            # Closes the database connection 
            con.close() 
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")

    
    # Searchs in the database for the 'student' where the roll is the same as the variable 'var_roll' and uses its data to fill the 'name' and 'course' variables
    def search_course(self):
        con = sqlite3.connect(database="rms.db")                        # Connects to the SQLite database
        cur = con.cursor()                                              # Creates a cursor object to interact with the database

        try:
            # Executes a SQL query to select the name and course from the student table where the roll matches the input
            cur.execute("select cid,description from course where name=?", (self.var_course_name.get(), ))
            row = cur.fetchone()                                        # Fetchs one result from the query
            
            # Checks if a row is returned
            if(row!=None):
                # Sets the 'name' and 'course' variables with the fetched data
                self.var_cid.set(row[0])
                self.var_course_description.set(row[1])
                
                self.course_txt_description.config(state=NORMAL)        # Temporarily enable the Text widget
                self.course_txt_description.delete('1.0', END)          # Clear the existing content
                self.course_txt_description.insert('1.0', self.var_course_description.get())  # Insert the new content
                self.course_txt_description.config(state=DISABLED)      # Set the Text widget back to readonly
            else:
                # Displays an error message if no record is found
                messagebox.showerror("Erro", "No record fond", parent=self.root)

            # Closes the database connection 
            con.close() 
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    # Adds the student enrollment into the 'enrollment' table in the database
    def add(self):
        con = sqlite3.connect(database="rms.db")                        # Connects to the SQLite database
        cur = con.cursor()                                              # Creates a cursor object to interact with the database

        try:
            # Checks if the 'name' variable is empty
            if (self.var_roll.get()=="" or self.var_cid.get()==""):
                # Displays an error message if the 'name' is empty
                messagebox.showerror("Erro", "Selecione um Estudante e um Curso", parent=self.root)
            else:
                # Execute a SQL query to check if the result already exists for the given roll and course
                cur.execute("select * from enrollment where roll=? and cid=?", (self.var_roll.get(), self.var_cid.get()))
                row = cur.fetchone()                                    # Fetchs one result from the query
                if (row!=None):
                    # If a result is found, display an error message indicating the result already exists
                    messagebox.showerror("Erro", "Inscrição já existe", parent=self.root)
                else:

                    # Executes a SQL query to insert the student 'result' into the 'result' table
                    cur.execute("insert into enrollment (roll, student_name, cid, course_name, course_description) values(?,?,?,?,?)", (
                                    self.var_roll.get(),
                                    self.var_student_name.get(),
                                    self.var_cid.get(),
                                    self.var_course_name.get(),
                                    self.var_course_description.get()
                                )
                            )
                    con.commit()                                        # Commit the transaction to save changes to the database

                    # Displays a success message indicating the course was added successfully
                    messagebox.showinfo("Sucesso", "Inscrição adicionada com sucesso", parent=self.root)

                    self.show()

                    # Closes the database connection 
                    con.close() 
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    # Searchs for a specific element in the 'enrollment table' with the provided 'course_name' element
    def search_enrollment_course(self):
        con = sqlite3.connect(database="rms.db")                            # Connects to the SQLite database
        cur = con.cursor()                                                  # Creates a cursor object to execute SQL queries

        try:
            # Executes SQL query to search for courses with names similar to the search input
            cur.execute(f"select * from enrollment where course_name LIKE '%{self.var_search_course.get()}%'")
            rows = cur.fetchall()                                                   # Fetch all the matching rows
            self.EnrollmentTable.delete(*self.EnrollmentTable.get_children())       # Clear the existing entries in the 'enrollment table widget'
            
            # Inserts the found record into the 'enrollment table widget' widget
            for row in rows:
                self.EnrollmentTable.insert('', END, values=row)

            # Closes the database connection 
            con.close() 
        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")
    

    # Searchs for a specific element in the 'enrollment table' with the provided 'roll' element
    def search_enrollment_student(self):
        con = sqlite3.connect(database="rms.db")                            # Connects to the SQLite database
        cur = con.cursor()                                                  # Creates a cursor object to execute SQL queries

        try:
            # Executes SQL query to search for enrollments with 'roll' similar to the search input
            cur.execute(f"select * from enrollment where roll LIKE '%{self.var_search_student.get()}%' or student_name LIKE '%{self.var_search_student.get()}%'")
            rows = cur.fetchall()                                                   # Fetch all the matching rows
            self.EnrollmentTable.delete(*self.EnrollmentTable.get_children())       # Clear the existing entries in the 'Treeview widget'
            
            # Inserts the found record into the 'enrollment table widget' widget
            for row in rows:
                self.EnrollmentTable.insert('', END, values=row)

            # Closes the database connection 
            con.close() 
        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    # Deletes a enrollment from the database with the same 'name' as the variable 'var_course'
    def delete(self):
        con = sqlite3.connect(database="rms.db")                            # Connect to the SQLite database
        cur = con.cursor()                                                  # Create a cursor object to execute SQL queries

        try:
            if (self.var_roll.get()=="" or self.var_cid.get()==""):
                messagebox.showerror("Erro", "Seleciona um Estudante e um Curso", parent=self.root)
            else:
                # Executes a SQL query to select all records from the 'enrollment' table with the same name as the 'enr_id' variable
                cur.execute("select * from enrollment where enr_id=?", (self.var_enr_id.get(), ))
                row = cur.fetchone()                                        # Fetchs the result
                if (row==None):
                    # If no enrollment is found shows an error message
                    messagebox.showerror("Erro", "Selecione uma inscrição da lista", parent=self.root)
                else:
                    # Asks for confirmation with a messagebox
                    op = messagebox.askyesno("Confirmar", "Você realmente deseja deletar?", parent=self.root)
                    if (op==True):
                        # Deletes the enrollment from the database where the row has the same name as the 'var_enr_id' variable 
                        cur.execute("delete from enrollment where enr_id=?", (self.var_enr_id.get(), ))
                        con.commit()                                        # Commits the changes
                        messagebox.showinfo("Deletar", "Inscrição deletada com sucesso", parent=self.root)
                        self.show()
                        self.clear()                                        # Clears the form fields (call the function 'clear')
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


    # Cleans all the variables and entry fields in the window
    def clear(self):
        self.var_enr_id.set("")
        self.var_roll.set("Select")                                     
        self.var_student_name.set("")                                           
        self.var_cid.set("Select")                                          
        self.var_course_name.set("")                                          
        self.var_course_description.set("")
        
        self.course_txt_description.config(state=NORMAL)            # Temporarily enable the Text widget
        self.course_txt_description.delete('1.0', END)              # Clear the existing content
        self.course_txt_description.config(state=DISABLED)          # Set the Text widget back to readonly


if __name__ == "__main__":
    root = Tk()
    obj = EnrollmentClass(root)
    root.mainloop()