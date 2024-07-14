from tkinter import *                           # Imports all classes, functions, and variables from the tkinter module
from PIL import Image,ImageTk                   # Imports the Image and ImageTk modules from the Python Imaging Library (PIL)
from tkinter import ttk                         # Import themed tkinter widgets
from tkinter import messagebox                  # Import messagebox for displaying message boxes
import sqlite3                                  # Imports the sqlite3 module, which is used for working with SQLite databases in Python

class ResultClass:
    def __init__(self, root):
        self.root = root                                                    # Initializes the root window
        self.root.title("Notas - Sistema de Gestão de Resultados")          # Title of the window
        self.root.geometry("1220x460")                                      # Dimensions of the window
        self.root.config(bg="white")                                        # Background color of the window
        self.root.focus_force()                                             # Forces the focus on the window
        self.root.resizable(False, False)
        
        # =============== Title ===============
        # Creates a label for the title and places it at the top of the window
        title = Label(self.root, 
                        text="Gerenciar Notas", 
                        font=("goudy old style",20,"bold"), 
                        bg="#033054", 
                        fg="white"
                    )
        title.place(x=10, y=15, width=1200, height=35)

        # =============== Variables ===============
        # Initialize the variables
        self.var_rid = StringVar()
        self.var_enr_id = StringVar()
        self.var_roll = StringVar()
        self.var_student_name = StringVar()
        self.var_cid = StringVar()
        self.var_course_name = StringVar()
        self.var_homework_grade = StringVar()
        self.var_participation_grade = StringVar()
        self.var_midterm_grade = StringVar()
        self.var_final_exam_grade = StringVar()
        self.var_total_grade = StringVar()

        self.roll_list = []                                                 # List to store the roll numbers
        self.course_list = []                                               # List to store the course numbers
        self.fetch_student()                                                # Calls the function (fetch_student) to fetch the roll numbers from the database
        self.fetch_course()                                                 # Calls the function (fetch_course) to fetch the course numbers from the database

        # =============== Group 1 ===============

        # --------------- Labels ---------------

        # Creates and places the label for the 'Select Students' field
        lbl_select = Label(self.root, text="Estudante", font=("goudy old style", 15, "bold"), bg="white")
        lbl_select.place(x=50, y=70)
        # Creates and places the label for the 'Student Name' field
        lbl_student_name = Label(self.root, text="Nome", font=("goudy old style", 15, "bold"), bg="white")
        lbl_student_name.place(x=50, y=110)
        # Creates and places the label for the 'Select Course' field
        lbl_course = Label(self.root, text="Curso", font=("goudy old style", 15, "bold"), bg="white")
        lbl_course.place(x=50, y=150)

        # --------------- Entry Fields  ---------------

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


        # =============== Separator ===============

        self.h_separator = ttk.Separator(self.root, orient="horizontal")
        self.h_separator.place(x=40, y=200, relwidth=0.47)


        # =============== Group 2 ===============

        # --------------- Labels ---------------

        # ............... Collumn 1 ...............

        # Creates the Label for the 'Nota Prova' entry
        lbl_nota_prova = Label(self.root, text="Nota Trabalhos", font=("goudy old style", 15, "bold"), bg="white")
        lbl_nota_prova.place(x=50, y=220)
        # Creates the Label for the 'Nota Trabalho' entry
        lbl_nota_trabalho = Label(self.root, text="Nota Testes", font=("goudy old style", 15, "bold"), bg="white")
        lbl_nota_trabalho.place(x=50, y=260)
        # Creates the Label for the 'Nota Participacao' entry
        lbl_nota_participacao = Label(self.root, text="Nota Total", font=("goudy old style", 15, "bold"), bg="white")
        lbl_nota_participacao.place(x=50, y=300)

        # ............... Collumn 2 ...............

        # Creates the Label for the 'State' entry
        lbl_nota_participacao = Label(self.root, text="Nota Participação", font=("goudy old style", 15, "bold"), bg="white")
        lbl_nota_participacao.place(x=350, y=220)
        # Creates the Label for the 'State' entry
        lbl_nota_total = Label(self.root, text="Nota Provas", font=("goudy old style", 15, "bold"), bg="white")
        lbl_nota_total.place(x=350, y=260)

        # --------------- Entry Fields  ---------------

        # ............... Collumn 1 ...............
        # Creates the entry field for the 'Nota Prova' field
        txt_nota_prova = Entry(self.root, textvariable=self.var_homework_grade, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_nota_prova.place(x=210, y=220, width=100)
        # Creates the entry field for the 'Nota Trabalho' field
        txt_nota_trabalho = Entry(self.root, textvariable=self.var_midterm_grade, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_nota_trabalho.place(x=210, y=260, width=100)
        # Creates the entry field for the 'Nota Participacao' field
        txt_nota_participacao = Entry(self.root, textvariable=self.var_total_grade, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_nota_participacao.place(x=210, y=300, width=100)


        # --------------- Collumn 2 ---------------

        # Creates the entry field for the course description
        txt_nota_participacao = Entry(self.root, textvariable=self.var_participation_grade, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_nota_participacao.place(x=510, y=220, width=100)

        txt_nota_total = Entry(self.root, textvariable=self.var_final_exam_grade, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_nota_total.place(x=510, y=260, width=100)


        # =============== Buttons ===============

        # Create and place the button to call the 'Submit' function (self.submit)
        self.btn_add = Button(self.root, text="Salvar", font=("times new roman", 15), bg="#2196f3", fg="white", cursor="hand2", command=self.submit)
        self.btn_add.place(x=50, y=400, width=120, height=35)
        # Create and place the button to call the 'Update' function (self.update)
        self.btn_update = Button(self.root, text="Atualizar", font=("times new roman", 15), bg="#4caf50", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=190, y=400, width=120, height=35)
        # Create and place the button to call the 'Delete' function (self.delete)
        self.btn_clear = Button(self.root, text="Deletar", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete)
        self.btn_clear.place(x=330, y=400, width=120, height=35)
        # Create and place the button to call the 'Clear' function (self.clear)
        self.btn_clear = Button(self.root, text="Limpar", font=("times new roman", 15), bg="#607d8b", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=470, y=400, width=120, height=35)


        # =============== Seach Panel ===============
    
        self.var_search_course = StringVar()                           # Variable to store the 'search course' query

        # Creates a label for the 'search course' field
        lbl_search_courseName = Label(self.root, text="Curso:", font=("Time News Roman", 11), bg="white")
        lbl_search_courseName.place(x=650, y=70)
        # Creates an entry field for the 'search course' input
        txt_search_courseName = Entry(self.root, textvariable=self.var_search_course, font=("goudy old style", 11, "bold"), bg="lightyellow")
        txt_search_courseName.place(x=710, y=70, width=110)
        # Creates the search button, which calls the 'search_enrollment_course' method
        self.btn_search = Button(self.root, text="Pesquisar", font=("goudy old style", 13, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.search_enrollment_course)
        self.btn_search.place(x=830, y=70, width=80, height=24)


        self.var_search_student = StringVar()                           # Variable to store the 'search student' query

        # Creates a label for the 'search student' field
        lbl_search_studentRoll = Label(self.root, text="Estudante:", font=("Time News Roman", 11), bg="white")
        lbl_search_studentRoll.place(x=920, y=70)
        # Creates an entry field for the 'search student' input
        txt_search_studentRoll = Entry(self.root, textvariable=self.var_search_student, font=("goudy old style", 11, "bold"), bg="lightyellow")
        txt_search_studentRoll.place(x=1000, y=70, width=100)
        # Creates the search button, which calls the 'search_enrollment_student' method
        self.btn_search = Button(self.root, text="Pesquisar", font=("goudy old style", 13, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.search_enrollment_student)
        self.btn_search.place(x=1110, y=70, width=80, height=24)


        # --------------- Course Table Widget ---------------
        
        # Creates a frame to hold the 'result table widget'
        self.R_Frame = Frame(self.root,
                                bd=2,
                                relief=RIDGE 
                            )
        self.R_Frame.place(x=651, y=110, width=540, height=325)

        # Creates vertical and horizontal scrollbars for the 'result table widget'
        scroll_y = Scrollbar(self.R_Frame, orient=VERTICAL)
        scroll_x = Scrollbar(self.R_Frame, orient=HORIZONTAL)

        # Creates a 'Treeview' widget for the 'result table widget' with the specified columns
        self.ResultTable = ttk.Treeview(self.R_Frame,
                                            columns=("rid", "enr_id", "roll", "student_name", "cid", "course_name", "homework_grade", "participation_grade", "midterm_grade", "final_exam_grade", "total_grade"),
                                            xscrollcommand=scroll_x.set,
                                            yscrollcommand=scroll_y.set
                                        )
        
        # Packs the scrollbars to the bottom and right sides of the frame
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.ResultTable.xview)                     # Configures the horizontal scrollbar to control the x view of the 'course table widget'
        scroll_y.config(command=self.ResultTable.yview)                     # Configures the vertical scrollbar to control the y view of the 'course table widget'

        # Defines the headings for the 'result table widget' columns
        self.ResultTable.heading("rid", text="Resultado ID")
        self.ResultTable.heading("enr_id", text="Inscrição ID")
        self.ResultTable.heading("roll", text="Estudante ID")
        self.ResultTable.heading("student_name", text="Nome do Estudante")
        self.ResultTable.heading("cid", text="Curso ID")
        self.ResultTable.heading("course_name", text="Nome do Curso")
        self.ResultTable.heading("homework_grade", text="Nota Trabalho")
        self.ResultTable.heading("participation_grade", text="Nota Participação")
        self.ResultTable.heading("midterm_grade", text="Nota Testes")
        self.ResultTable.heading("final_exam_grade", text="Nota Prova")
        self.ResultTable.heading("total_grade", text="Nota Total")

        # Displays only the headings (no index column)
        self.ResultTable["show"] = 'headings'
        # Sets the width for each column
        self.ResultTable.column("rid", width=100)
        self.ResultTable.column("enr_id", width=100)
        self.ResultTable.column("roll", width=100)
        self.ResultTable.column("student_name", width=150)
        self.ResultTable.column("cid", width=100)
        self.ResultTable.column("course_name", width=150)
        self.ResultTable.column("homework_grade", width=150)
        self.ResultTable.column("participation_grade", width=150)
        self.ResultTable.column("midterm_grade", width=150)
        self.ResultTable.column("final_exam_grade", width=150)
        self.ResultTable.column("total_grade", width=150)

        self.ResultTable.pack(fill=BOTH, expand=1)                          # Packs the 'result table widget' to fill the frame
        self.ResultTable.bind("<ButtonRelease-1>", self.get_data)           # Binds a click event to the 'result table widget' to call the 'get_data' method
        self.show()                                                             # Calls the 'show' method to populate the table with data


    # When a row in the course table is clicked, this method is called. It sets the entry fields in the form with the data from the selected row.
    def get_data(self, ev):

        r = self.ResultTable.focus()                                        # Gets the currently selected row in the 'result table widget'
        content = self.ResultTable.item(r)                                  # Retrieves the item data for the selected row
        row = content["values"]                                                 # Extracts the values from the item data

        # Sets the form fields with the data from the selected row
        self.var_rid.set(row[0])
        self.var_enr_id.set(row[1])
        self.var_roll.set(row[2])
        self.var_student_name.set(row[3])
        self.var_cid.set(row[4])
        self.var_course_name.set(row[5])
        self.var_homework_grade.set(row[6])
        self.var_participation_grade.set(row[7])
        self.var_midterm_grade.set(row[8])
        self.var_final_exam_grade.set(row[9])
        self.var_total_grade.set(row[10])


    # This function fetches all the records from the 'result' table in the database and populates the 'result table widget' with this data
    def show(self):
        con = sqlite3.connect(database="rms.db")                                    # Connects to the SQLite database
        cur = con.cursor()                                                          # Creates a cursor object to interact with the database

        try:
            cur.execute("select * from result")                                     # Executes a SQL query to select all records from the 'result' table
            rows = cur.fetchall()                                                   # Fetch all the rows returned by the query
            self.ResultTable.delete(*self.ResultTable.get_children())               # Clears the current content of the 'result' table

            # Loop through the rows
            for row in rows:
                self.ResultTable.insert('', END, values=row)                    # Inserts each row into the 'result' table

            # Closes the database connection 
            con.close()
        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")                # Shows an error message if an exception occurs


    # Method called when an option of the "student combobox" is selected
    def on_student_selected(self, event):
        self.search_student()


    # Method called when an option of the "course combobox" is selected
    def on_course_selected(self, event):
        con = sqlite3.connect(database="rms.db")                        # Connects to the SQLite database
        cur = con.cursor()                                              # Creates a cursor object to interact with the database

        try:
            # Execute a SQL query to check if there's an existing 'course' for the given 'course name'
            cur.execute("select * from course where name=?", (self.var_course_name.get(), ))
            row = cur.fetchone()                                    # Fetchs one result from the query
            if (row==None):
                # If no course is found, display an error message
                messagebox.showerror("Erro", "Curso não encontrado", parent=self.root)
            else:
                # Get the value of 'var_cid' from the 'course' table and put it in the local variable 'var_cid'
                self.var_cid.set(row[0])
                con.close() 
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")

    
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
                    # Appends the roll number to the 'roll_list'
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
            # Execute a SQL query to select all 'name' numbers from the 'course' table
            cur.execute("select name from course")
            rows = cur.fetchall()                                       # Fetchs all the results of the query

            # Check if any rows are returned
            if (len(rows)>0):
                # Loops through each row in the results
                for row in rows:
                    # Appends the cid number to the 'course_list'
                    self.course_list.append(row[0])
        
            # Closes the database connection 
            con.close() 
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")
    

    # Searchs in the database for the 'student' where the roll is the same as the variable 'var_roll' and uses its data to fill the 'var_student_name' variables
    def search_student(self):
        con = sqlite3.connect(database="rms.db")                        # Connects to the SQLite database
        cur = con.cursor()                                              # Creates a cursor object to interact with the database

        try:
            # Executes a SQL query to select the 'name' from the student table where the 'roll' matches the input
            cur.execute("select name from student where roll=?", (self.var_roll.get(), ))
            row = cur.fetchone()                                        # Fetchs one result from the query
            
            # Checks if a row is returned
            if(row!=None):
                # Sets the 'name' variables with the fetched data
                self.var_student_name.set(row[0])
            else:
                # Displays an error message if no record is found
                messagebox.showerror("Erro", "No record fond", parent=self.root)

            # Closes the database connection 
            con.close() 
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    # Searchs for a specific element in the 'course table' with the provided 'course name' element
    def search_enrollment_course(self):
        con = sqlite3.connect(database="rms.db")                            # Connects to the SQLite database
        cur = con.cursor()                                                  # Creates a cursor object to execute SQL queries

        try:
            # Executes SQL query to search for courses with names similar to the search input
            cur.execute(f"select * from result where course_name LIKE '%{self.var_search_course.get()}%'")
            rows = cur.fetchall()                                           # Fetch all the matching rows
            self.ResultTable.delete(*self.ResultTable.get_children())       # Clear the existing entries in the 'Treeview widget'
            
            # Inserts the found record into the 'result table widget' widget
            for row in rows:
                self.ResultTable.insert('', END, values=row)

            # Closes the database connection 
            con.close() 
        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")
    

    # Searchs for a specific element in the 'enrollment table' with the provided 'roll' or 'student_name' element
    def search_enrollment_student(self):
        con = sqlite3.connect(database="rms.db")                                    # Connects to the SQLite database
        cur = con.cursor()                                                          # Creates a cursor object to execute SQL queries

        try:
            # Executes SQL query to search for students with 'name' or 'roll' similar to the search input
            cur.execute(f"select * from enrollment where roll LIKE '%{self.var_search_student.get()}%' or student_name LIKE '%{self.var_search_student.get()}%'")
            rows = cur.fetchall()                                                   # Fetch all the matching rows
            self.ResultTable.delete(*self.ResultTable.get_children())               # Clear the existing entries in the 'Treeview widget'
            
            # Inserts the found record into the 'result table widget' widget
            for row in rows:
                self.ResultTable.insert('', END, values=row)

            # Closes the database connection 
            con.close() 
        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    # Adds the student grades into the 'result' table in the database
    def submit(self):
        con = sqlite3.connect(database="rms.db")                            # Connects to the SQLite database
        cur = con.cursor()                                                  # Creates a cursor object to interact with the database

        try:
            # Checks if the 'var_roll' or 'var_cid' variable is empty
            if (self.var_roll.get()=="" or self.var_cid.get()==""):
                # Displays an error message if the 'name' or 'cid' is empty
                messagebox.showerror("Erro", "Selecione um Estudante e Curso", parent=self.root)
            else:
                # Execute a SQL query to check if there's an existing 'enrollment' for the given 'roll' and 'course'
                cur.execute("select * from enrollment where roll=? and cid=?", (self.var_roll.get(), self.var_cid.get()))
                row = cur.fetchone()                                        # Fetchs one result from the query
                if (row==None):
                    # If no enrollment is found, display an error message
                    messagebox.showerror("Erro", "Inscrição não encontrada", parent=self.root)
                else:
                    # Get the value of 'enr_id' from the 'enrollment' table and put it in the variable 'var_enr_id'
                    self.var_enr_id.set(row[0])

                    cur.execute("select * from result where enr_id=?", (self.var_enr_id.get(),))
                    row = cur.fetchone()                                    # Fetchs one result from the query
                    if (row!=None):
                        # If a result is found, display an error message indicating that the result already exists
                        messagebox.showerror("Erro", "Resultado já existe para esta inscrição, por favor a atualize", parent=self.root)
                    else:
                        # Executes a SQL query to insert the student grades into the 'result' table
                        cur.execute("insert into result (enr_id, roll, student_name, cid, course_name, homework_grade, participation_grade, midterm_grade, final_exam_grade, total_grade) values(?,?,?,?,?,?,?,?,?,?)", (
                                        self.var_enr_id.get(),
                                        self.var_roll.get(),
                                        self.var_student_name.get(),
                                        self.var_cid.get(),
                                        self.var_course_name.get(),
                                        self.var_homework_grade.get(),
                                        self.var_participation_grade.get(),
                                        self.var_midterm_grade.get(),
                                        self.var_final_exam_grade.get(),
                                        self.var_total_grade.get()
                                    )
                                )
                        con.commit()                                        # Commit the transaction to save changes to the database

                        # Displays a success message indicating the Result was added successfully
                        messagebox.showinfo("Sucesso", "Resultado adicionado com sucesso", parent=self.root)

                        self.show()

                        # Closes the database connection 
                        con.close() 
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    # Updates the student grades into the 'result' table in the database
    def update(self):
        con = sqlite3.connect(database="rms.db")                        # Connects to the SQLite database
        cur = con.cursor()                                              # Creates a cursor object to interact with the database

        try:
            if(self.var_rid.get()==""):
                messagebox.showerror("Erro", "Selecione um resultado da lista", parent=self.root)
            else:
                if (self.var_roll.get()=="" or self.var_cid.get()==""):
                    # Displays an error message if the 'name' or 'cid' is empty
                    messagebox.showerror("Erro", "Estudante e Curso necessários", parent=self.root)
                else:
                    # Executes a SQL to select the element in the 'result' table with the same rid as 'var_rid'
                    cur.execute("select * from result where rid=?", (self.var_rid.get(), ))
                    row = cur.fetchone()
                    if (row==None):
                        # Displays an error message if no 'result' is selected from the list
                        messagebox.showerror("Erro", "Resultado inválido selecionado", parent=self.root)
                    else:
                        # Executes a SQL to update the 'result' details in the 'result' table
                        cur.execute("update result set enr_id=?, roll=?, student_name=?, cid=?, course_name=?, homework_grade=?, participation_grade=?, midterm_grade=?, final_exam_grade=?, total_grade=?", (
                                        self.var_enr_id.get(),
                                        self.var_roll.get(),
                                        self.var_student_name.get(),
                                        self.var_cid.get(),
                                        self.var_course_name.get(),
                                        self.var_homework_grade.get(),
                                        self.var_participation_grade.get(),
                                        self.var_midterm_grade.get(),
                                        self.var_final_exam_grade.get(),
                                        self.var_total_grade.get()
                                    )
                                )
                        con.commit()                                            # Commits the transaction
                        messagebox.showinfo("Sucesso", "Resultado atualizado com sucesso", parent=self.root)
                        self.show()                                             # Calls the function 'self.show()' to update the 'student table widget'

                        # Closes the database connection 
                        con.close() 
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    # Deletes a result from the database with the same 'rid' as the variable 'var_rid'
    def delete(self):
        con = sqlite3.connect(database="rms.db")                            # Connect to the SQLite database
        cur = con.cursor()                                                  # Create a cursor object to execute SQL queries

        try:
            if(self.var_rid.get()==""):
                messagebox.showerror("Erro", "Selecione um resultado da lista", parent=self.root)
            else:
                # Executes a SQL query to select all records from the 'resulr' table with the same name as the 'var_rid' variable
                cur.execute("select * from result where rid=?", (self.var_rid.get(), ))
                row = cur.fetchone()                                        # Fetchs the result
                if (row==None):
                    # If no 'result' is found shows an error message
                    messagebox.showerror("Erro", "Selecione um resultado da lista", parent=self.root)
                else:
                    # Asks for confirmation with a messagebox
                    op = messagebox.askyesno("Confirm", "Do you really wanna delete?", parent=self.root)
                    if (op==True):
                        # Deletes the 'result' from the database where the row has the same 'rid' as the 'var_rid' variable 
                        cur.execute("delete from result where rid=?", (self.var_rid.get(), ))
                        con.commit()                                        # Commits the changes
                        messagebox.showinfo("Deletar", "Resultado deletado com sucesso", parent=self.root)
                        self.show()
                        self.clear()                                        # Clears the form fields (call the function 'clear')
        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    # Cleans all the variables and entry fields in the window
    def clear(self):
        self.var_rid.set("")
        self.var_enr_id.set("")
        self.var_roll.set("Select")  
        self.var_student_name.set("") 
        self.var_cid.set("") 
        self.var_course_name.set("Select")
        self.var_homework_grade.set("") 
        self.var_participation_grade.set("") 
        self.var_midterm_grade.set("") 
        self.var_final_exam_grade.set("") 
        self.var_total_grade.set("")

        self.roll_list.clear()                                          # Clear the course list
        self.txt_student.set("Select")                                  # Reset the combobox to the default value
        self.fetch_student()
        self.txt_student['values'] = self.roll_list                     # Update the combobox values

        self.course_list.clear()                                        # Clear the course list
        self.txt_course.set("Select")                                   # Reset the combobox to the default value
        self.fetch_course()
        self.txt_course['values'] = self.course_list                    # Update the combobox values


if __name__ == "__main__":
    root = Tk()
    obj = ResultClass(root)
    root.mainloop()