from tkinter import *                   # Import all classes, functions, and variables from tkinter
from PIL import Image, ImageTk          # Import Image and ImageTk from PIL for handling images
from tkinter import ttk                 # Import themed tkinter widgets
from tkinter import messagebox          # Import messagebox for displaying message boxes
import sqlite3                          # Import sqlite3 for database operations
import os                               # Import os for interacting with the operating system
import shared


class Login_Window:
    def __init__(self, root):
        self.root = root                                                    # The "root" window object   
        self.root.title("Login - Sistema de Gestão de Resultados")          # Title of the window
        self.root.geometry("650x480")                                       # Geometry of the window (width x height)
        self.root.focus_force()                                             # Forces the focus on the window
        self.root.resizable(False, False)
        
        # =============== Frame ===============

        # Creates and place a frame in the middle of the window
        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=0, y=0, width=650, height=500)

        # --------------- Title ---------------

        # Create and place the title label with the 'logo image'
        title = Label(login_frame, 
                        text="Login", 
                        font=("goudy old style",20,"bold"), 
                        bg="#B00857", 
                        fg="white",
                        compound=LEFT,
                        padx=10
                    )
        title.place(x=10, y=15, width=630, height=50)

        # --------------- Content ---------------

        # Adds a label and entry field for the email address
        email = Label(login_frame, text="Email", font=("times new roman", 18, "bold"), bg="white", fg="gray")
        email.place(x=150, y=125)
        self.txt_email = Entry(login_frame, font=("times new roman", 15, "bold"), bg="lightgray")
        self.txt_email.place(x=150, y=160, width=350, height=35)

        # Adds a label and entry field for the password
        password = Label(login_frame, text="Senha", font=("times new roman", 18, "bold"), bg="white", fg="gray")
        password.place(x=150, y=225)
        self.txt_password = Entry(login_frame, font=("times new roman", 15, "bold"), bg="lightgray")
        self.txt_password.place(x=150, y=260, width=350, height=35)

        # Adds a button for registering a new account (calls the function 'register_window')
        btn_reg = Button(login_frame, text="Registrar?", font=("times new roman", 14), bg="white", bd=0, fg="#B00857", cursor="hand2", command=self.register_window)
        btn_reg.place(x=150, y=300)

        # Add a button for forgetting the password (calls the function 'forget_password_window')
        btn_forget = Button(login_frame, text="Esqueceu Senha?", font=("times new roman", 14), bg="white", bd=0, fg="red", cursor="hand2", command=self.forget_password_window)
        btn_forget.place(x=350, y=300)

        # Add a button for logging in (calls the function 'login')
        self.btn_login = Button(login_frame, text="Login", font=("goudy old style", 15, "bold"), bg="#B00857", fg="white", cursor="hand2", command=self.login)
        self.btn_login.place(x=150, y=360, width=200, height=40)


    # This method clears all the input fields and resets the security question combo box to its default state.
    def reset(self):
        self.cmb_quest.current(0)                   # Set the current selection of the security question combo box to the first option (index 0)
        self.txt_new_password.delete(0, END)        # Clear the new password entry field
        self.txt_answer.delete(0, END)              # Clear the answer entry field
        self.txt_password.delete(0, END)            # Clear the password entry field
        self.txt_email.delete(0, END)               # Clear the email entry field


    #  This method closes the current login window and opens the registration window by running register.py.
    def register_window(self):
        self.root.destroy()                         # Destroy the current window
        os.system("python register.py")             # Run the register.py script to open the registration window


    # This method handles the logic for resetting a user's password.
    def forget_password(self):
        # Checks if any field is empty
        if(self.cmb_quest.get()=="Select" or self.txt_answer.get()=="" or self.txt_new_password.get()==""):
            # If any field is empty, shows an error message
            messagebox.showerror("Erro", "Todos os campos são necessarios", parent=self.root2)
        else:
            try:
                # Connect to the SQLite database
                con = sqlite3.connect(database="rms.db")        
                cur = con.cursor()
                # Executes a query to find the user with the provided email, security question, and answer
                cur.execute("select * from employee where email=? and question=? and answer=?", (self.txt_email.get(), self.cmb_quest.get(), self.txt_answer.get()))
                row = cur.fetchone()

                # Checks if the user exists
                if(row==None):
                    # If the user does not exist, shows an error message
                    messagebox.showerror("Erro", "Plese select the current security question/answer", parent=self.root2)
                else:
                    # If the user exists, update the password
                    cur.execute("update employee set password=? where email=? and question=? and answer=?", (self.txt_new_password.get(), self.txt_email.get(), self.cmb_quest.get(), self.txt_answer.get()))
                    con.commit()                                    # Commit the changes to the database
                    con.close()                                     # Close the database connection
                    messagebox.showerror("Success", "Password has been reset. Please login with the new password", parent=self.root2)
                    self.reset()                                    # Reset all input fields (calls the function 'reset')
                    self.root2.destroy()                            # Destroy the 'forget password' window
            except Exception as ex:
                # If an error occurs, show an error message
                messagebox.showerror("Erro", f"Error due to {str(ex)}", parent=self.root)


    # This method creates a new window for resetting the password if a valid email address is provided.
    def forget_password_window(self):
        # Checks if the email field is empty
        if(self.txt_email.get()==""):
            # If empty, show an error message
            messagebox.showerror("Erro", "Insira um endereço de email válido para resetar o password", parent=self.root)
        else:
            try:
                # Connects to the SQLite database
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                # Executes a query to check if the provided email exists in the database
                cur.execute("select * from employee where email=?", (self.txt_email.get(),))
                row = cur.fetchone()

                # Checks if the email exists in the database
                if(row==None):
                    # If not, shows an error message
                    messagebox.showerror("Erro", "Insira um endereço de email válido para resetar o password", parent=self.root)
                else:
                    con.close()                                         # Closes the database connection

                    # =============== Forgot Password Window ===============

                    self.root2 = Toplevel()                             # Toplevel window is a separate, independent window that appears on top of other windows in the application.
                    self.root2.title("Esqueceu Senha")
                    self.root2.geometry("350x420+495+150")
                    self.root2.config(bg="white")
                    self.root2.focus_force()                            # Focus on the new window
                    self.root2.grab_set()                               # Prevent interactions with other windows until this window is close

                    # --------------- Title ---------------

                    title = Label(self.root2, 
                        text="Esqueceu Senha", 
                        font=("goudy old style",20,"bold"), 
                        bg="red", 
                        fg="white",
                        compound=LEFT,
                        padx=10
                    )
                    title.place(x=10, y=15, width=330, height=50)

                    # --------------- Content ---------------

                    # Labels and entry fields for security question, answer, and new password
                    question = Label(self.root2, text="Pergunta de Segurança", font=("times new roman", 15, "bold"), bg="white", fg="gray")
                    question.place(x=50, y=95)
                    self.cmb_quest = ttk.Combobox(self.root2, font=("times new roman", 13), state="readonly", justify=CENTER)
                    self.cmb_quest['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name")
                    self.cmb_quest.place(x=50, y=125, width=255)
                    self.cmb_quest.current(0)

                    answer = Label(self.root2, text="Resposta", font=("times new roman", 15, "bold"), bg="white", fg="gray")
                    answer.place(x=50, y=175)
                    self.txt_answer = Entry(self.root2, font=("times new roman", 15), bg="lightgray")
                    self.txt_answer.place(x=50, y=205, width=255)

                    new_password = Label(self.root2, text="Nova Senha", font=("times new roman", 15, "bold"), bg="white", fg="gray")
                    new_password.place(x=50, y=255)
                    self.txt_new_password = Entry(self.root2, font=("times new roman", 15), bg="lightgray")
                    self.txt_new_password.place(x=50, y=285, width=255)

                    # Button to reset the password (calls the function 'forget_password')
                    btn_change_password = Button(self.root2, text="Confirmar", font=("times new roman", 15, "bold"), fg="white", bg="red", cursor="hand2", command=self.forget_password)
                    btn_change_password.place(x=100, y=345, width=150)

            except Exception as ex:
                # If an error occurs, show an error message
                messagebox.showerror("Erro", f"Error due to {str(ex)}", parent=self.root)


    # This method handles the logic for authenticating the user's login credentials.
    def login(self):
        # Checks if email or password fields are empty
        if (self.txt_email.get()=="" or self.txt_password.get()==""):
            # If any field is empty, show an error message
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos", parent=self.root)
        else:
            try:
                # Connects to the SQLite database
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                # Executes a query to find the user with the given email and password
                cur.execute("select * from employee where email=? and password=?", (self.txt_email.get(), self.txt_password.get()))
                row = cur.fetchone()

                # Checks if the user exists
                if(row==None):
                    # If the user does not exist, shows an error message
                    messagebox.showerror("Erro", "Invalid Username or Password", parent=self.root)
                else:
                    # If the user exists, shows a success message
                    messagebox.showinfo("Sucesso", f"Logado com sucesso - Bem-vindo: {self.txt_email.get()}", parent=self.root)

                    shared.var_eid = row[0]
                    
                    # Destroy all elements in the current window
                    for widget in self.root.winfo_children():
                        widget.destroy()

                    import dashboard
                    dashboard_obj = dashboard.RMS(self.root)

                con.close()                                             # Closes the database connection
            except Exception as ex:
                # If an error occurs, show an error message
                messagebox.showerror("Erro", f"Error due to {str(ex)}", parent=self.root)


# Checks if the script is being run as the main program
if __name__ == "__main__":
    root = Tk()                                                         # Creates the main Tkinter window object, which serves as the parent window for all other widgets
    obj = Login_Window(root)                                            # This initializes and sets up the login window interface
    root.mainloop()                                                     # This line starts the Tkinter event loop, which listens for events and updates the GUI