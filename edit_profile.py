from tkinter import *                   # Import all classes, functions, and variables from tkinter
from tkinter import ttk                 # Import themed tkinter widgets
from tkinter import messagebox          # Import messagebox for displaying message boxes
import sqlite3                          # Import sqlite3 for database operations
import os                               # Import os for interacting with the operating system
import shared

class EditClass:
    def __init__(self, root):
        self.root = root                                                # Sets the title of the window
        self.root.title("Editar Perfil")                                # Sets the size of the window    
        self.root.geometry("700x420")                                   # Sets the background color of the window
        self.root.config(bg="white")                                    # Sets the background color of the window
        self.root.focus_force()                                         # Forces the focus on the window
        self.root.resizable(False, False)

        # =============== Variables ===============
        self.var_eid = shared.var_eid

        # =============== Edit Profile Frame ===============
        # Creates a frame for the registration form with a white background
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=0, y=0, width=700, height=440)

        # --------------- Title ---------------
        # Creates a Label widget for the title of the registration form
        title = Label(frame1, text="Editar Perfil", font=("times new roman", 20, "bold"), bg="green", fg="white")
        title.place(x=20, y=20, width=650, height=40)

        # --------------- Row 1 ---------------
        # Creates a Label widget and an Entry widget for the user to input the 'name'
        name = Label(frame1, text="Nome", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        name.place(x=50, y=80)
        self.txt_name = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_name.place(x=50, y=110, width=250)

        # Creates a Label widget and an Entry widget for the user to input the 'address'
        address = Label(frame1, text="Endereço", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        address.place(x=370, y=80)
        self.txt_address = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_address.place(x=370, y=110, width=250)

        # --------------- Row 2 ---------------
        # Create a Label widget and an Entry widget for the user to input the 'contact number'
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

        # Create a Label widget and an Entry widget for the user to input the 'position'
        position = Label(frame1, text="Posição", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        position.place(x=50, y=220)
        self.cmb_position = ttk.Combobox(frame1, font=("times new roman", 13), state="readonly", justify=CENTER)
        self.cmb_position['values'] = ("Select", "Administrator", "Manager", "Teacher")
        self.cmb_position.place(x=50, y=250, width=250)
        self.cmb_position.current(0)  # Set the default value of the combobox to "Select"


        # --------------- Update Profile Button ---------------
        btn_update = Button(frame1, text="Atualizar Perfil", font=("goudy old style", 15, "bold"), bg="green", fg="white", cursor="hand2", command=self.update_data)
        btn_update.place(x=50, y=330, width=180)

        self.fetch_employee_data()

        # --------------- Clear Button ---------------
        btn_clear = Button(frame1, text="Limpar", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.clear)
        btn_clear.place(x=250, y=330, width=180)


    def fetch_employee_data(self):
        try:
            con = sqlite3.connect(database="rms.db")  # Connects to the SQLite database
            cur = con.cursor()  # Create a cursor object to interact with the database
            cur.execute("SELECT name, adress, contact, email, question, answer, password, position FROM employee WHERE eid=?", (self.var_eid,))
            row = cur.fetchone()
        
            if (row):
                self.txt_name.insert(END, row[0])
                self.txt_address.insert(END, row[1])
                self.txt_contact.insert(END, row[2])
                self.txt_email.insert(END, row[3])
                self.cmb_position.set(row[7])

            con.close()  # Closes the database connection
        except Exception as ex:
            # Shows error message if an exception occurs
            messagebox.showerror("Erro", f"Error due to {str(ex)}", parent=self.root)


    # Updates the employee's data in the 'employee' table
    def update_data(self):
        # Checks if any required field is empty
        if (self.txt_name.get() == "" or self.txt_contact.get() == "" or self.txt_email.get() == "" or self.txt_address.get() == "" or self.cmb_position.get() == "Select"):
            messagebox.showerror("Erro", "Todos os campos são necessarios", parent=self.root)
        # Checks if 'password' and 'confirm password' fields match
        else:
            try:
                con = sqlite3.connect(database="rms.db")  # Connects to the SQLite database
                cur = con.cursor()  # Create a cursor object to interact with the database
                # Update the user data in the 'employee' table
                cur.execute(""" UPDATE employee SET name=?, adress=?, contact=?, email=?, position=? WHERE eid=? """, (
                    self.txt_name.get(),
                    self.txt_address.get(),
                    self.txt_contact.get(),
                    self.txt_email.get(),
                    self.cmb_position.get(),
                    self.var_eid
                ))
                con.commit()            # Commits the transaction
                con.close()             # Closes the database connection

                messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso", parent=self.root)

            except Exception as ex:
                # Shows error message if an exception occurs
                messagebox.showerror("Erro", f"Error due to {str(ex)}", parent=self.root)


    # Clears all the entry fields in the registration form.
    def clear(self):
        self.txt_name.delete(0, END)
        self.txt_address.delete(0, END)
        self.txt_contact.delete(0, END)
        self.txt_email.delete(0, END)
        self.cmb_position.current(0)


if __name__ == "__main__":
    root = Tk()
    obj = EditClass(root)
    root.mainloop()
