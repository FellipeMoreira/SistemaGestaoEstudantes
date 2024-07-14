from tkinter import *                           # Imports all classes, functions, and variables from the tkinter module
from PIL import Image, ImageTk                  # Imports the Image and ImageTk modules from the Python Imaging Library (PIL)
from tkinter import ttk                         # Import themed tkinter widgets
from tkinter import messagebox                  # Import messagebox for displaying message boxes
import sqlite3                                  # Imports the sqlite3 module, which is used for working with SQLite databases in Python

class GradeClass:
    def __init__(self, root):
        self.root = root                                                    # Initializes the root window
        self.root.title("Boletim - Result Management System")                # Title of the window
        self.root.geometry("1320x570")                                      # Dimensions of the window
        self.root.config(bg="white")                                        # Background color of the window
        self.root.focus_force()                                             # Forces the focus on the window
        self.root.resizable(False, False)

        # =============== Title ===============
        # Creates and place the title label
        title = Label(self.root, 
                        text="Gerenciar Boletim", 
                        font=("goudy old style",20,"bold"), 
                        bg="orange", 
                        fg="#262626"
                    )
        title.place(x=10, y=15, width=1300, height=35)

        # =============== Variables ===============
        # Initializes the variables
        self.var_search = StringVar()
        self.var_id = ""
        self.var_student_name = StringVar()

        self.roll_list = []
        self.fetch_student()

        # =============== Search ===============
        # Creates and place the 'search' label
        self.lbl_search_student = Label(self.root, text="No. Estudante:", font=("goudy old style", 20, "bold"), bg="white")
        self.lbl_search_student.place(x=50, y=100)
        # Combobox for selecting a student
        self.txt_search_student = ttk.Combobox(self.root, textvariable=self.var_search, values=self.roll_list, font=("goudy old style", 20, "bold"), state='readonly', justify=CENTER)
        self.txt_search_student.place(x=240, y=100, width=200)
        self.txt_search_student.set("Select")
        self.txt_search_student.bind("<<ComboboxSelected>>", self.on_student_selected)

        # Creates and place the 'search' label
        self.lbl_student_name = Label(self.root, text="Name:", font=("goudy old style", 20, "bold"), bg="white")
        self.lbl_student_name.place(x=480, y=100)
        # Creates and places the entry fields for the student name
        self.txt_student_name = Entry(self.root, textvariable=self.var_student_name, font=("goudy old style", 20, "bold"), bg="lightyellow", state="readonly")
        self.txt_student_name.place(x=580, y=100, width=200)

        # Creates and place the 'search' button (calls the 'self.search' function)
        self.btn_search = Button(self.root, text="Pesquisar", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.search)
        self.btn_search.place(x=820, y=98, width=100, height=40)
        # Creates and place the 'clear' button (calls the 'self.clear' function)
        self.btn_clear = Button(self.root, text="Limpar", font=("goudy old style", 15, "bold"), bg="gray", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=940, y=98, width=100, height=40)

        # =============== Main Frame ===============
        # Replace your current placement of main_frame with the following:
        self.main_frame = Frame(self.root, bg="white", highlightthickness=1, highlightbackground="black")
        self.main_frame.place(x=50, y=170, width=1220, height=350)

        # Scrollbar
        self.canvas = Canvas(self.main_frame, bg="white")
        self.scrollbar = Scrollbar(self.main_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)


    def create_rows(self, data):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Column Labels with adjustable size
        labels = ["No. Estudante", "Nome", "Curso", "Trabalhos", "Participação", "Testes", "Provas", "Total"]
        column_widths = [150] * len(labels)                                         # Adjust widths as needed
        column_heights = [50] * len(labels)                                         # Initial heights for column labels

        for i, (label, width, height) in enumerate(zip(labels, column_widths, column_heights)):
            Label(self.scrollable_frame, text=label, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).grid(row=0, column=i, sticky="nsew")
            self.scrollable_frame.columnconfigure(i, weight=1, minsize=width)       # Adjust width
            self.scrollable_frame.rowconfigure(0, weight=1, minsize=height)         # Adjust height for column labels

        # Data rows with adjustable height
        for row_num, row_data in enumerate(data, start=1):
            # Exclude the first (ID), second (Roll), and fifth elements
            filtered_data = [row_data[i] for i in range(len(row_data)) if i not in {0, 1, 4}]
            
            for col_num, value in enumerate(filtered_data, start=0):
                label = Label(self.scrollable_frame, text=value, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
                label.grid(row=row_num, column=col_num, sticky="nsew")
                self.scrollable_frame.rowconfigure(row_num, weight=1, minsize=50)   # Adjust height for data rows


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


    # Method called when an option of the "student combobox" is selected
    def on_student_selected(self, event):
        con = sqlite3.connect(database="rms.db")                        # Connects to the SQLite database
        cur = con.cursor()                                              # Creates a cursor object to interact with the database

        try:
            # Executes a SQL query to select the 'name' from the student table where the 'roll' matches the input
            cur.execute("select name from student where roll=?", (self.var_search.get(), ))
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

    
    def search(self):
        con = sqlite3.connect(database="rms.db")                        # Connect to the database
        cur = con.cursor()                                              # Creates a cursor object to interact with the database

        try:
            if (self.var_search.get() == ""):
                messagebox.showerror("Erro", "No. Estudante é necessário", parent=self.root)
            else:
                cur.execute("select * from result where roll=?", (self.var_search.get(),))
                rows = cur.fetchall()

                if rows:
                    self.create_rows(rows)
                else:
                    messagebox.showerror("Erro", "Resultado não encontrado", parent=self.root)
                con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


    def clear(self):
        self.var_id = ""                                        # Resets the variable that stores the current 'record ID'
        
        # Clear search entry field
        self.txt_search_student.delete(0, 'end')                # Clear the entry widget itself
        self.txt_search_student.set("Select")                   # Reset the combobox to the default value
        self.var_student_name.set("") 
        self.var_search.set("")                                 # Clear the text in the search variable

        # Clear scrollable frame content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()


    def delete(self):
        con = sqlite3.connect(database="rms.db")                        # Connect to the database
        cur = con.cursor()                                              # Creates a cursor object to interact with the database

        try:
            if (self.var_id == ""):
                messagebox.showerror("Erro", "Procure por um estudante válido", parent=self.root)
            else:
                cur.execute("select * from result where rid=?", (self.var_id,))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Erro", "Resultado não encontrado", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirmar", "Você realmente deseja deletar?", parent=self.root)
                    if op == True:
                        cur.execute("delete from result where rid=?", (self.var_id,))
                        con.commit()

                        messagebox.showinfo("Deletar", "Resultados deletados com sucesso", parent=self.root)
                        self.clear()
                con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


if __name__ == "__main__":
    root = Tk()
    obj = GradeClass(root)
    root.mainloop()
