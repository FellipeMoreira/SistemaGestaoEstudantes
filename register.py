from tkinter import *                   # Import all classes, functions, and variables from tkinter
from PIL import Image, ImageTk          # Import Image and ImageTk from PIL for handling images
from tkinter import ttk                 # Import themed tkinter widgets
from tkinter import messagebox          # Import messagebox for displaying message boxes
import sqlite3                          # Import sqlite3 for database operations
import os                               # Import os for interacting with the operating system

class Register:
    def __init__(self, root):
        self.root = root                                                    # Sets the title of the window
        self.root.title("Registrar - Sistema de Gestão de Resultados")      # Sets the size of the window    
        self.root.geometry("700x600")                                       # Sets the background color of the window
        self.root.config(bg="white")                                        # Sets the background color of the window
        self.root.focus_force()                                             # Forces the focus on the window
        self.root.resizable(False, False)
        
        # =============== Register Frame ===============
        # Creates a frame for the registration form with a white background
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=0, y=0, width=700, height=600)

        # --------------- Title ---------------
        # Creates a Label widget for the title of the registration form

        # Create and place the title label with the 'logo image'
        title = Label(frame1, 
                        text="Registrar", 
                        font=("goudy old style",20,"bold"), 
                        bg="green", 
                        fg="white",
                        compound=LEFT,
                        padx=10
                    )
        title.place(x=10, y=15, width=680, height=50)
        
        # --------------- Row 1 ---------------
        # Creates a Label widget and an Entry widget for the user to input the 'first name'
        name = Label(frame1, text="Nome", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        name.place(x=50, y=80)
        self.txt_name = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_name.place(x=50, y=110, width=250)

        # Creates a Label widget and an Entry widget for the user to input the 'adress'
        adress = Label(frame1, text="Endereço", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        adress.place(x=370, y=80)
        self.txt_adress = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_adress.place(x=370, y=110, width=250)

        # --------------- Row 2 ---------------
        # Create a Label widget and a an Entry widget for the user to input the 'contact number'
        contact = Label(frame1, text="Contato No.", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        contact.place(x=50, y=150)
        self.txt_contact = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_contact.place(x=50, y=180, width=250)

        # Create a Label widget and an Entry widget for the user to input the 'email address'
        email = Label(frame1, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        email.place(x=370, y=150)
        self.txt_email = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=370, y=180, width=250)

        # --------------- Row 3 ---------------

        # Create a Label widget and a an Entry widget for the user to input the 'contact number'
        position = Label(frame1, text="Posição", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        position.place(x=50, y=220)
        self.cmb_position = ttk.Combobox(frame1, font=("times new roman", 13), state="readonly", justify=CENTER)
        self.cmb_position['values'] = ("Select", "Administrator", "Manager", "Teacher")
        self.cmb_position.place(x=50, y=250, width=250)
        self.cmb_position.current(0)                                       # Set the default value of the combobox to "Select"

        # --------------- Row 4 ---------------
        # Create a Label widget for the 'security question'
        question = Label(frame1, text="Pergunta de Segurança", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        question.place(x=50, y=310)
        # Create a Combobox widget for the user to select a 'security question'
        self.cmb_quest = ttk.Combobox(frame1, font=("times new roman", 13), state="readonly", justify=CENTER)
        self.cmb_quest['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name")
        self.cmb_quest.place(x=50, y=340, width=250)
        self.cmb_quest.current(0)                                       # Set the default value of the combobox to "Select"

        # Creates a Label widget and an Entry widget for the user to input the 'security answer'
        answer = Label(frame1, text="Resposta", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        answer.place(x=370, y=310)
        self.txt_answer = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_answer.place(x=370, y=340, width=250)

        # --------------- Row 5 ---------------
        # Creates a Label and an Entry widget for the user to input the 'password'
        password = Label(frame1, text="Senha", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        password.place(x=50, y=380)
        self.txt_password = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_password.place(x=50, y=410, width=250)

        # Create a Label and an Entry widget for the user to input the 'confirm password'
        cpassword = Label(frame1, text="Confirmar Senha", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        cpassword.place(x=370, y=380)
        self.txt_cpassword = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_cpassword.place(x=370, y=410, width=250)

        # --------------- Terms & Conditions ---------------
        # Creates a Checkbutton widget for agreeing to the 'terms and conditions'
        self.var_chk = IntVar()
        chk = Checkbutton(frame1, text="Eu concordo com os Termos & Condiçoes", variable=self.var_chk, onvalue=1, offvalue=0, bg="white", font=("times new roman", 12))
        chk.place(x=50, y=450)

        # --------------- Register Button ---------------
        btn_login = Button(frame1, text="Registrar", font=("goudy old style", 15, "bold"), bg="green", fg="white", cursor="hand2", command=self.register_data)
        btn_login.place(x=50, y=510, width=180)

        # --------------- Login Button ---------------
        # Create a Button widget for 'login'
        btn_login = Button(frame1, text="Login", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.login_window)
        btn_login.place(x=250, y=510, width=180)



    # Opens the 'login window'.
    def login_window(self):
        self.root.destroy()                         # Destroy the current window
        os.system("python login.py")                # Executes the command to run the 'login' script, which opens the 'login window'

    # Clears all the entry fields in the registration form.
    def clear(self):
        self.txt_name.delete(0, END)
        self.txt_adress.delete(0, END)
        self.txt_contact.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_answer.delete(0, END)
        self.txt_password.delete(0, END)
        self.txt_cpassword.delete(0, END)
        self.cmb_quest.current(0)

    # Registers the data from the 'registration form' into the 'employee' table
    def register_data(self):
        # Checks if any required field is empty
        if (self.txt_name.get()=="" or self.txt_contact.get()=="" or self.txt_email.get()=="" or self.txt_answer.get()=="" or self.txt_password.get()=="" or self.txt_cpassword.get()=="" or self.cmb_quest.get()=="Select"):
            messagebox.showerror("Erro", "Preencha todos os campos", parent=self.root)
        # Checks if 'password' and 'confirm password' fields match
        elif (self.txt_password.get() != self.txt_cpassword.get()):
            messagebox.showerror("Erro", "Senha & Confirmar Senha devem ser o mesmo", parent=self.root)
        # Checks if the 'terms and conditions' checkbox is checked
        elif (self.var_chk.get()==0):
            messagebox.showerror("Erro", "Você deve concordar com os Termos & Condições", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database="rms.db")                                            # Connects to the SQLite database
                cur = con.cursor()                                                                  # Create a cursor object to interact with the database
                cur.execute("select * from employee where email=?", (self.txt_email.get(), ))       # Executes a SQL query to check if there is any existing user with the entered email
                row = cur.fetchone()                                                                # Fetch one record from the result of the query

                if(row!=None):
                    # Shows error message if the 'email' is already registered
                    messagebox.showerror("Erro", "Usuario já cadastrado, utilize outro email", parent=self.root)
                else:
                    # Insert the new user data into the 'employee' table
                    cur.execute("insert into employee (name, adress, contact, email, question, answer, password, position) values(?,?,?,?,?,?,?,?)", (
                                    self.txt_name.get(),
                                    self.txt_adress.get(),
                                    self.txt_contact.get(),
                                    self.txt_email.get(),
                                    self.cmb_quest.get(),
                                    self.txt_answer.get(),
                                    self.txt_password.get(),
                                    self.cmb_position.get()
                                )
                            )
                    con.commit()                    # Commits the transaction
                    con.close()                     # Closes the database connection
                    messagebox.showerror("Successo", "Registro Completo", parent=self.root)
                    self.clear()                    # Clears all the 'registration form' fields (calls the function clear)
                    self.login_window()             # Opens the 'login window'
            except Exception as ex:
                # Shows error message if an exception occurs
                messagebox.showerror("Erro", f"Error due to {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Register(root)
    root.mainloop()