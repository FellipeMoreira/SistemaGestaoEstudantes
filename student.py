from tkinter import *                           # Imports all classes, functions, and variables from the tkinter module
from PIL import Image,ImageTk                   # Imports the Image and ImageTk modules from the Python Imaging Library (PIL)
from tkinter import ttk                         # Import themed tkinter widgets
from tkinter import messagebox                  # Import messagebox for displaying message boxes
import sqlite3                                  # Imports the sqlite3 module, which is used for working with SQLite databases in Python

class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Estudantes - Sistema de Gestão de Resultados")               # Title of the window
        self.root.geometry("1200x480")                                      # Dimensions of the window
        self.root.config(bg="white")                                        # Background color of the window
        self.root.focus_force()                                             # Forces the focus on the window
        self.root.resizable(False, False)
        
        # =============== Title ===============
        # Title label at the top of the application
        title = Label(self.root, 
                        text="Gerenciar Estudantes", 
                        font=("goudy old style",20,"bold"), 
                        bg="#033054", 
                        fg="white"
                    )
        title.place(x=10, y=15, width=1180, height=35)

        # =============== Variables ===============
        # Initializes the variables to hold student information
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_a_date = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()

        # =============== Labels ===============

        # --------------- Column 1 ---------------
        # Creates the Label for the 'Roll No' entry
        lbl_roll = Label(self.root, text="No. Estudante", font=("goudy old style", 15, "bold"), bg="white")
        lbl_roll.place(x=10, y=60)
        # Creates the Label for the 'Name' entry
        lbl_name = Label(self.root, text="Nome", font=("goudy old style", 15, "bold"), bg="white")
        lbl_name.place(x=10, y=100)
        # Creates the Label for the 'Email' entry
        lbl_email = Label(self.root, text="Email", font=("goudy old style", 15, "bold"), bg="white")
        lbl_email.place(x=10, y=140)
        # Creates the Label for the 'Gender' entry
        lbl_gender = Label(self.root, text="Gênero", font=("goudy old style", 15, "bold"), bg="white")
        lbl_gender.place(x=10, y=180)
        # Creates the Label for the 'State' entry
        lbl_state = Label(self.root, text="Estado", font=("goudy old style", 15, "bold"), bg="white")
        lbl_state.place(x=10, y=220)
        # Creates the Label for the 'Adress' entry
        lbl_adress = Label(self.root, text="Endereço", font=("goudy old style", 15, "bold"), bg="white")
        lbl_adress.place(x=10, y=260)

        # --------------- Column 2 ---------------
        # Creates the Label for the 'D.O.B' entry
        lbl_dob = Label(self.root, text="Data de Nascimento", font=("goudy old style", 15, "bold"), bg="white")
        lbl_dob.place(x=380, y=60)
        # Creates the Label for the 'Contact' entry
        lbl_contact = Label(self.root, text="Contato", font=("goudy old style", 15, "bold"), bg="white")
        lbl_contact.place(x=380, y=100)
        # Creates the Label for the 'Admission' entry
        lbl_addmission = Label(self.root, text="Adimissão", font=("goudy old style", 15, "bold"), bg="white")
        lbl_addmission.place(x=380, y=140)
        # Creates the Label for the 'City' entry
        lbl_city = Label(self.root, text="Cidade", font=("goudy old style", 15, "bold"), bg="white")
        lbl_city.place(x=380, y=180)
        # Creates the Label for the 'Pin' entry
        lbl_pin = Label(self.root, text="CEP", font=("goudy old style", 15, "bold"), bg="white")
        lbl_pin.place(x=380, y=220)

        # =============== Entry Fields ===============

        # --------------- Column 1 ---------------
        # Creates an Entry Field for the 'var_roll' variable
        self.txt_roll = Entry(self.root, textvariable=self.var_roll, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_roll.place(x=150, y=60, width=200)
        # Creates an Entry Field for the 'var_name' variable
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_name.place(x=150, y=100, width=200)
        # Creates an Entry Field for the 'var_email' variable
        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_email.place(x=150, y=140, width=200)
        # Creates an Entry Field for the 'var_gender' variable
        self.txt_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Others"), font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_gender.place(x=150, y=180, width=200)
        self.txt_gender.current(0)
        # Creates an Entry Field for the 'var_state' variable
        txt_state = Entry(self.root, textvariable=self.var_state, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_state.place(x=150, y=220, width=150)
        # Creates a Text Field for the 'txt_adress' variable
        self.txt_adress = Text(self.root, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_adress.place(x=150, y=260, width=530, height=100)

        # --------------- Column 2 ---------------
        # Creates an Entry Field for the 'var_dob' variable
        self.txt_dob = Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_dob.place(x=560, y=60, width=120)
        # Creates an Entry Field for the 'var_contact' variable
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_contact.place(x=480, y=100, width=200)
        # Creates an Entry Field for the 'var_a_date' variable
        txt_addmission = Entry(self.root, textvariable=self.var_a_date, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_addmission.place(x=480, y=140, width=200)
        # Creates an Entry Field for the 'var_city' variable
        txt_city = Entry(self.root, textvariable=self.var_city, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_city.place(x=480, y=180, width=110)
        # Creates an Entry Field for the 'var_pin' variable
        txt_pin = Entry(self.root, textvariable=self.var_pin, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_pin.place(x=480, y=220, width=110)

        # =============== Buttons ===============
        # Creates a button to save the new student data (call the function 'self.add')
        self.btn_add = Button(self.root, text="Salvar", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.add)
        self.btn_add.place(x=150, y=400, width=110, height=40)
        # Creates a button to updates a student data (call the function 'self.update')
        self.btn_update = Button(self.root, text="Atualizar", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=270, y=400, width=110, height=40)
        # Creates a button to delete a student data (call the function 'self.delete')
        self.btn_delete = Button(self.root, text="Deletar", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=390, y=400, width=110, height=40)
        # Creates a button to clear a new student (call the function 'self.clear')
        self.btn_clear = Button(self.root, text="Limpar", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=510, y=400, width=110, height=40)

        # =============== Seach Panel ===============
        self.var_search = StringVar()                               # Variable for search input

        # Creates the Label for the search field
        lbl_search_roll = Label(self.root, text="No. Estudante", font=("goudy old style", 15, "bold"), bg="white")
        lbl_search_roll.place(x=720, y=60)
        # Entry field for user to input the roll number for searching
        txt_search_roll = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_search_roll.place(x=870, y=60, width=180)
        # Button to call the search action (self.search)
        self.btn_search = Button(self.root, text="Pesquisar", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.search)
        self.btn_search.place(x=1070, y=60, width=120, height=28)

        # =============== Student Table Widget ===============
        # Creates a frame to contain the table and its scrollbars
        self.C_Frame = Frame(self.root,
                                bd=2,
                                relief=RIDGE 
                            )
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        # Scrollbars for the table
        scroll_y = Scrollbar(self.C_Frame, orient=VERTICAL)
        scroll_x = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        # Treeview widget for displaying tabular data
        self.CourseTable = ttk.Treeview(self.C_Frame,
                                            columns=("roll", "name", "email", "gender", "dob", "contact", "admission", "state", "city", "pin", "address"),
                                            xscrollcommand=scroll_x.set,
                                            yscrollcommand=scroll_y.set
                                        )
        
        # Attaches scrollbars to the 'student table widget'
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.CourseTable.xview)
        scroll_y.config(command=self.CourseTable.yview)

        # Configuring the column headings for the 'student table widget'
        self.CourseTable.heading("roll", text="No. Estudante")
        self.CourseTable.heading("name", text="Nome")
        self.CourseTable.heading("email", text="Email")
        self.CourseTable.heading("gender", text="Gênero")
        self.CourseTable.heading("dob", text="Data de Nascimento")
        self.CourseTable.heading("contact", text="Contato")
        self.CourseTable.heading("admission", text="Adimissão")
        self.CourseTable.heading("state", text="Estado")
        self.CourseTable.heading("city", text="Cidade")
        self.CourseTable.heading("pin", text="CEP")
        self.CourseTable.heading("address", text="Endereço")

        # Displaying only the headings
        self.CourseTable["show"] = 'headings'

        # Configuring the widths of the columns in the 'student table widget'
        self.CourseTable.column("roll", width=120)
        self.CourseTable.column("name", width=100)
        self.CourseTable.column("email", width=100)
        self.CourseTable.column("gender", width=100)
        self.CourseTable.column("dob", width=150)
        self.CourseTable.column("contact", width=100)
        self.CourseTable.column("admission", width=100)
        self.CourseTable.column("state", width=100)
        self.CourseTable.column("city", width=100)
        self.CourseTable.column("pin", width=100)
        self.CourseTable.column("address", width=200)

        self.CourseTable.pack(fill=BOTH, expand=1)                          # Packing the table to fill the frame
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)           # Binding a function to trigger when a row in the table is clicked
        self.show()                                                         # Calls the function to populate the table with data


    # Retrivwes the contects of the selected row and updates the entry fields in the window
    def get_data(self, ev):
        # Setting the 'roll' field to readonly mode
        self.txt_roll.config(state="readonly")

        r = self.CourseTable.focus()                                        # Gets the focus of the table
        content = self.CourseTable.item(r)                                  # Retrieves the content of the selected row
        row = content["values"]                                             # Atributes the contents of the row to a variable (list) 'row'

        # Sets the values of the selected row into its respective variables and fields
        self.var_roll.set(row[0]),
        self.var_name.set(row[1]),
        self.var_email.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_dob.set(row[4]),
        self.var_contact.set(row[5]),
        self.var_a_date.set(row[6]),
        self.var_state.set(row[7]),
        self.var_city.set(row[8]),
        self.var_pin.set(row[9]),
        self.txt_adress.delete("1.0", END)                                  # Clears and inserts the text to the 'address' field
        self.txt_adress.insert(END, row[10])


    # Shows/Updates the current entries in the 'student table widget'
    def show(self):
        con = sqlite3.connect(database="rms.db")                            # Connects to the SQLite database
        cur = con.cursor()                                                  # Creates a cursor object to interact with the database

        try:
            # Executs a SQL query to retrieve all rows from the 'student' table
            cur.execute("select * from student")
            rows = cur.fetchall()
            # Delets all the current entries in the 'student table widget'
            self.CourseTable.delete(*self.CourseTable.get_children())
            # Inserts the fetched rows into the 'student table widget'
            for row in rows:
                self.CourseTable.insert('', END, values=row)
                
            # Closes the database connection 
            con.close() 
        except Exception as ex:
            # Displaying an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    # Adds a new student to the 'student' table, if there's no other with the same 'roll' as the variable 'var_roll'
    def add(self):
        con = sqlite3.connect(database="rms.db")                            # Connects to the SQLite database
        cur = con.cursor()                                                  # Creates a cursor object to interact with the database

        try:
            # Checks if the 'roll number' field is empt
            if (self.var_roll.get()==""):
                # Displays an error message if the 'roll number' is empty
                messagebox.showerror("Erro", "No. Estudante é necessário", parent=self.root)
            else:
                # Executes a SQL to select the element in the 'student table' with the same roll as 'var_roll'
                cur.execute("select * from student where roll=?", (self.var_roll.get(), ))
                row = cur.fetchone()
                if (row!=None):
                    # If it finds such a roll, it displays an error message saying that the roll number already exists
                    messagebox.showerror("Erro", "No. Estudante já existe", parent=self.root)
                else:
                    # Executes a SQL to insert the student details into the 'student' table
                    cur.execute("insert into student (roll, name, email, gender, dob, contact, admission, state, city, pin, address) values(?,?,?,?,?,?,?,?,?,?,?)", (
                                    self.var_roll.get(),
                                    self.var_name.get(),
                                    self.var_email.get(),
                                    self.var_gender.get(),
                                    self.var_dob.get(),
                                    self.var_contact.get(),
                                    self.var_a_date.get(),
                                    self.var_state.get(),
                                    self.var_city.get(),
                                    self.var_pin.get(),
                                    self.txt_adress.get("1.0", END)
                                )
                            )
                    con.commit()                                            # Commits the transaction
                    messagebox.showinfo("Sucesso", "Exstudante adicionado com sucesso", parent=self.root)
                    self.show()                                             # Calls the function 'self.show()' to update the 'student table widget'

                    # Closes the database connection 
                    con.close() 
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    # Adds the row in the 'student' table with the same 'roll' as the variable 'var_roll'
    def update(self):
        con = sqlite3.connect(database="rms.db")                            # Connects to the SQLite database
        cur = con.cursor()                                                  # Creates a cursor object to interact with the database

        try:
            # Checks if the 'roll number' field is empty
            if (self.var_roll.get()==""):
                # Displays an error message if the 'roll number' is empty
                messagebox.showerror("Erro", "No. Estudante é necessário", parent=self.root)
            else:
                # Executes a SQL to select the element in the 'student table' with the same roll as 'var_roll'
                cur.execute("select * from student where roll=?", (self.var_roll.get(), ))
                row = cur.fetchone()
                if (row==None):
                    # Displays an error message if no student is selected from the list
                    messagebox.showerror("Erro", "Selecione um estudante da lista", parent=self.root)
                else:
                    # Executes a SQL to update the student details in the 'student' table
                    cur.execute("update student set name=?, email=?, gender=?, dob=?, contact=?, admission=?, state=?, city=?, pin=?, address=? where roll=?", (
                                    self.var_name.get(),
                                    self.var_email.get(),
                                    self.var_gender.get(),
                                    self.var_dob.get(),
                                    self.var_contact.get(),
                                    self.var_a_date.get(),
                                    self.var_state.get(),
                                    self.var_city.get(),
                                    self.var_pin.get(),
                                    self.txt_adress.get("1.0", END),
                                    self.var_roll.get()
                                )
                            )
                    con.commit()                                            # Commits the transaction
                    messagebox.showinfo("Sucesso", "Estudante atualizado com sucesso", parent=self.root)
                    self.show()                                             # Calls the function 'self.show()' to update the 'student table widget'

                    # Closes the database connection 
                    con.close() 
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")
    

    #  Clear all the variables and entry fields and refreshes the 'student table widget'
    def clear(self):
        # Calls the function 'self.show()' to update the 'student table widget'
        self.show()
        # Resets the values of all input fields and variables to default or empty
        self.var_roll.set(""),
        self.var_name.set(""),
        self.var_email.set(""),
        self.var_gender.set("Select"),
        self.var_dob.set(""),
        self.var_contact.set(""),
        self.var_a_date.set(""),
        self.var_state.set(""),
        self.var_city.set(""),
        self.var_pin.set(""),
        self.txt_adress.delete("1.0", END)
        self.txt_roll.config(state=NORMAL)
        self.var_search.set("")

    
    # Deletes a student from the database with the same 'roll' as the variable 'var_roll'
    def delete(self):
        con = sqlite3.connect(database="rms.db")                            # Connects to the SQLite database
        cur = con.cursor()                                                  # Creates a cursor object to interact with the database

        try:
            # Checks if the 'roll number' field is empty
            if (self.var_roll.get()==""):
                # Displays an error message if the 'roll number' is empty
                messagebox.showerror("Erro", "No. Estudante é necessário", parent=self.root)
            else:
                # Executes a SQL to select the element in the 'student' table with the same roll as 'var_roll'
                cur.execute("select * from student where roll=?", (self.var_roll.get(), ))
                row = cur.fetchone()
                if (row==None):
                    # Displays an error message if no student with the provided roll number is found
                    messagebox.showerror("Erro", "Selecione um estudante da lista", parent=self.root)
                else:
                    # Asks for confirmation before deleting the student
                    op = messagebox.askyesno("Confirmar", "Você realmente deseja deletar?", parent=self.root)
                    if (op==True):
                        # Executes a SQL to delete the student from the 'student' table
                        cur.execute("delete from student where roll=?", (self.var_roll.get(), ))
                        con.commit()                                        # Commits the transaction
                        messagebox.showinfo("Deletar", "Curso deletado com sucesso", parent=self.root)
                        self.clear()                                        # Calls the 'clear' method to reset the input fields in the window
        except Exception as ex:
            # Displays an error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    def search(self):
        con = sqlite3.connect(database="rms.db")                            # Connects to the SQLite database
        cur = con.cursor()                                                  # Creates a cursor object to execute SQL queries

        try:
            # Executes SQL query to search for courses with names similar to the search input
            cur.execute(f"select * from student where roll LIKE '%{self.var_search.get()}%'")
            rows = cur.fetchall()                                           # Fetch all the matching rows
            self.CourseTable.delete(*self.CourseTable.get_children())       # Clear the existing entries in the 'Treeview widget'
            
            # Inserts the found record into the 'course table widget' widget
            for row in rows:
                self.CourseTable.insert('', END, values=row)

            # Closes the database connection 
            con.close() 
        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


if __name__ == "__main__":
    root = Tk()
    obj = StudentClass(root)
    root.mainloop()