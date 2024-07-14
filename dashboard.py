from tkinter import *                       # Imports all classes, functions, and variables from the tkinter module
from PIL import Image,ImageTk               # Imports the Image and ImageTk modules from the Python Imaging Library (PIL)
from course import CourseClass              # Imports the CourseClass class from the 'course' module
from student import StudentClass            # Imports the StudentClass class from the 'student' module
from result import ResultClass              # Imports the ResultClass class from the 'result' module
from enrollment import EnrollmentClass      # Imports the EnrollmentClass class from the 'enrollment' module
from grades import GradeClass               # Imports the GradeClass class from the 'grades' module
from report import ReportClass              # Imports the ReportClass class from the 'report' module
from edit_profile import EditClass          # Imports the EditClass class from the 'edit_profile' module
from tkinter import messagebox              # Imports the messagebox module from tkinter
import os                                   # Imports the os module, which provides functions for interacting with the operating system
import sqlite3                              # Imports the sqlite3 module, which is used for working with SQLite databases in Python
import shared                               # module for the sahred variables
from tkinter import filedialog              # Import filedialog for opening file dialogs
import base64                               # For encoding and decoding image data
import io                                   # For handling byte data

#RMS - Result Management System
class RMS:
    def __init__(self, root):
        self.root = root                                                        # Sets the main window instance to the root attribute of the class
        self.root.title("Sistema de Gestão de Resultados de Estudantes")        # Sets the title of the main window
        self.root.geometry("1350x710")                                          # Sets the dimensions of the main window
        self.root.config(bg="white")                                            # Sets the background color of the main window to white
        self.root.resizable(False, False)
        
        # =============== Title ===============
        # Create and place the title label with the 'logo image'
        title = Label(self.root, 
                        text="Sistema de Gestão de Resultados de Estudantes", 
                        font=("goudy old style",20,"bold"), 
                        bg="#033054", 
                        fg="white",
                        #image=self.logo_dash,
                        compound=LEFT,
                        padx=10
                    )
        title.place(x=10, y=15, width=1330, height=50)
        

        # =============== Variables ===============
        self.logged_in = False                                  # Variable to track login status, initially set to False
        self.var_eid = shared.var_eid

        # =============== Menu ===============

        # Create a LabelFrame for the menu buttons
        self.M_Frame = LabelFrame(self.root,
                                text="Menu",
                                font=("Times New Roman", 15),
                                bg="white" 
                            )
        self.M_Frame.place(x=20, y=70, width=246, height=560)

        # --------------- Buttons ---------------

        # Button that calls the 'add_course' function (Add Courses)
        self.btn_course = Button(self.M_Frame, text="Add. Cursos", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_course)
        self.btn_course.place(x=20, y=5, width=200, height=40)
        # Button that calls the 'add_student' function (Add Students)
        self.btn_student = Button(self.M_Frame, text="Add. Estudantes", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_student)
        self.btn_student.place(x=20, y=50, width=200, height=40)
        # Button that calls the 'add_enrollment' function (Add Enrollment)
        self.btn_enrollment = Button(self.M_Frame, text="Add. Inscrição", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_enrollment)
        self.btn_enrollment.place(x=20, y=95, width=200, height=40)
        # Button that calls the 'add_result' function (Add Reports)
        self.btn_result = Button(self.M_Frame, text="Add. Notas", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_result)
        self.btn_result.place(x=20, y=140, width=200, height=40)
        # Button that calls the 'view_grades' function (logout from the dashboard)
        self.btn_grade = Button(self.M_Frame, text="Ver Boletims", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.view_grade)
        self.btn_grade.place(x=20, y=185, width=200, height=40)
        # Button that calls the 'view_report' function (Exits the program)
        self.btn_report = Button(self.M_Frame, text="Ver Relatórios", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.view_report)
        self.btn_report.place(x=20, y=230, width=200, height=40)
        # Button that calls the 'exit_program' function (Exits the program)
        self.btn_exit = Button(self.M_Frame, text="Exit", font=("goudy old style", 15, "bold"), bg="dark red", fg="white", cursor="hand2", command=self.exit_program)
        self.btn_exit.place(x=20, y=320, width=200, height=40)

        # =============== Profile ===============
        
        # Create a LabelFrame for the menu buttons
        self.P_Frame = LabelFrame(self.root,
                                text="Perfil",
                                font=("Times New Roman", 15),
                                bg="white" 
                            )
        self.P_Frame.place(x=290, y=70, width=1000, height=400)

        # --------------- Content ---------------

        # Creates the label for the Photo 
        self.photo_label = Label(self.P_Frame, text="No Image", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=SOLID)
        self.photo_label.place(x=10, y=10, width=280, height=280)

        # Creates the label for the 'Employee Name'
        self.lbl_employee_name = Label(self.P_Frame, text="Bem-vindo: [Employee Name]", font=("goudy old style", 15, "bold"), bg="white")
        self.lbl_employee_name.place(x=320, y=10)
        # Creates the label for the 'Employee Role'
        self.lbl_employee_role = Label(self.P_Frame, text="Posição: [Employee Role/Position]", font=("goudy old style", 15, "bold"), bg="white")
        self.lbl_employee_role.place(x=320, y=60)
        # Creates the label for the 'Employee Contact'
        self.lbl_employee_contact = Label(self.P_Frame, text="Contato: [Employee Email/Phone]", font=("goudy old style", 15, "bold"), bg="white")
        self.lbl_employee_contact.place(x=320, y=110)
        # Creates the label for the 'Employee - Total Courses'
        self.lbl_employee_courses = Label(self.P_Frame, text="Total de Cursos: [Numero]", font=("goudy old style", 15, "bold"), bg="white")
        self.lbl_employee_courses.place(x=320, y=160)
        # Creates the label for the 'Employee - Courses: [List]'
        self.lbl_employee_courses_list = Label(self.P_Frame, text="Cursos: [Lista]", font=("goudy old style", 15, "bold"), bg="white")
        self.lbl_employee_courses_list.place(x=320, y=210)
        # Creates the label for the 'Employee - Total Students'
        self.lbl_employee_students = Label(self.P_Frame, text="Total de Estudantes: [Numero]", font=("goudy old style", 15, "bold"), bg="white")
        self.lbl_employee_students.place(x=320, y=260)

        # Button that calls the 'upload_photo' function (Uploads the photo)
        self.btn_upload_photo = Button(self.P_Frame, text="Carregar Foto", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.upload_photo)
        self.btn_upload_photo.place(x=10, y=310, width=200, height=40)
        # Button that calls the 'exit_program' function (Exits the program)
        self.btn_edit_profile = Button(self.P_Frame, text="Editar Perfil", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.edit_profile)
        self.btn_edit_profile.place(x=220, y=310, width=200, height=40)
        # Button that calls the 'logout' function (logout from the dashboard)
        self.btn_logout = Button(self.P_Frame, text="Logout", font=("goudy old style", 15, "bold"), bg="gray", fg="white", cursor="hand2", command=self.logout)
        self.btn_logout.place(x=430, y=310, width=200, height=40)

        # =============== Login? ===============
        
        # Create a LabelFrame for the menu buttons
        self.L_Frame = LabelFrame(self.root,
                                text="Perfil",
                                font=("Times New Roman", 15),
                                bg="white" 
                            )
        self.L_Frame.place(x=290, y=70, width=1000, height=400)

        self.btn_login = Button(self.L_Frame, text="Login", font=("times new roman", 20, "bold"), fg="white", bg="#0b5377", cursor="hand2", command=self.open_login_window)
        self.btn_login.place(relx=0.5, rely=0.5, width=250, height=100, anchor=CENTER)

        self.check_login_status()

        # =============== Details ===============
        
        # Create a LabelFrame for the menu buttons
        self.D_Frame = LabelFrame(self.root,
                                text="Detalhes",
                                font=("Times New Roman", 15),
                                bg="white" 
                            )
        self.D_Frame.place(x=290, y=470, width=1000, height=160)

        # --------------- Update Details ---------------
        # Create a Label that show the total amount of courses registred
        self.lbl_course = Label(self.D_Frame, text="Total de Cursos\n[ 0 ]", font=("goudy old style", 20), bd=10, relief=RIDGE, bg="#e43b06", fg="white")
        self.lbl_course.place(x=22, y=12, width=300, height=100)
        # Create a Label that show the total amount of students registred
        self.lbl_students = Label(self.D_Frame, text="Total de Estudantes\n[ 0 ]", font=("goudy old style", 20), bd=10, relief=RIDGE, bg="#0676ad", fg="white")
        self.lbl_students.place(x=346, y=12, width=300, height=100)
        # Create a Label that show the total amount of results registred
        self.lbl_results = Label(self.D_Frame, text="Total de Inscrições\n[ 0 ]", font=("goudy old style", 20), bd=10, relief=RIDGE, bg="#038074", fg="white")
        self.lbl_results.place(x=672, y=12, width=300, height=100)

        # --------------- Updates ---------------

        self.update_details()                               # Updates the details everytime the dashboard is loaded (calls the function update_details)
        self.update_employee_details()

    # =============== App Windows ===============

    # Calls the CourseClass window
    def add_course(self):
        self.new_win = Toplevel(self.root)                  # Creates a new top-level window as a child of the main window
        self.new_obj = CourseClass(self.new_win)            # Instantiate the CourseClass with the new window

    # Calls the StudentClass window
    def add_student(self):
        self.new_win = Toplevel(self.root)                  # Creates a new top-level window as a child of the main window
        self.new_obj = StudentClass(self.new_win)           # Instantiate the StudentClass with the new window

    # Calls the ResultClass window
    def add_enrollment(self):
        self.new_win = Toplevel(self.root)                  # Creates a new top-level window as a child of the main window
        self.new_obj = EnrollmentClass(self.new_win)            # Instantiate the ResultClass with the new window
        
    # Calls the ReportClass window
    def add_result(self):
        self.new_win = Toplevel(self.root)                  # Creates a new top-level window as a child of the main window
        self.new_obj = ResultClass(self.new_win)            # Instantiate the ReportClass with the new window

    # Calls the ReportClass window
    def view_grade(self):
        self.new_win = Toplevel(self.root)                  # Creates a new top-level window as a child of the main window
        self.new_obj = GradeClass(self.new_win)            # Instantiate the ReportClass with the new window

    # Calls the ReportClass window
    def view_report(self):
        self.new_win = Toplevel(self.root)                  # Creates a new top-level window as a child of the main window
        self.new_obj = ReportClass(self.new_win)            # Instantiate the ReportClass with the new window

    # Calls the ReportClass window
    def edit_profile(self):
        self.new_win = Toplevel(self.root)                  # Creates a new top-level window as a child of the main window
        self.new_obj = EditClass(self.new_win)            # Instantiate the ReportClass with the new window

    # Leaves the 'dashboard' and returns to the 'login window'
    def logout(self):
        # Ask the user for confirmation to logout
        op = messagebox.askyesno("Confirmar","Você realmente deseja sair?", parent=self.root)
        # If the user confirms
        if (op==True):
            self.root.destroy()                                 # Destroy the main window
            os.system("python login.py")                        # Run the 'login.py' script to show the login window

    # Exits the program
    def exit_program(self):
        # Ask the user for confirmation to exit the program
        op = messagebox.askyesno("Confirmar","Você realmente deseja sair do programa?", parent=self.root)
        # If the user confirms
        if (op==True):
            self.root.destroy()                                 # Destroy the main window and exit the program


    # =============== Details Update ===============

    # Updates the labels to display the total number of courses, students, and results fetched from the database.
    def update_details(self):
        con = sqlite3.connect(database="rms.db")                # Connect to the SQLite database
        cur = con.cursor()                                      # Create a cursor object to execute SQL queries

        try:
            cur.execute("select * from course")                                         # Execute SQL query to select all records from the 'course' table
            cr = cur.fetchall()                                                         # Fetch all the records returned by the query
            self.lbl_course.config(text=f"Total de Cursos\n[{str(len(cr))}]")           # Update the label to display the total number of courses

            cur.execute("select * from student")                                        # Execute SQL query to select all records from the 'student' table
            cr = cur.fetchall()                                                         # Fetch all the records returned by the query
            self.lbl_students.config(text=f"Total de Estudantes\n[{str(len(cr))}]")     # Update the label to display the total number of students

            cur.execute("select * from enrollment")                                     # Execute SQL query to select all records from the 'result' table
            cr = cur.fetchall()                                                         # Fetch all the records returned by the query
            self.lbl_results.config(text=f"Total de Inscrições\n[{str(len(cr))}]")      # Update the label to display the total number of results

            # Schedule the update_details method to be called again after 200 milliseconds
            self.lbl_course.after(200, self.update_details)

            # Closes the database connection 
            con.close() 
        except Exception as ex:
            # Display an error message if there's an exception while updating details
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    def update_employee_details(self):
        if (self.var_eid is not None):
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            try:
                # Fetch employee details including the photo
                cur.execute("SELECT name, position, contact, email, photo FROM employee WHERE eid = ?", (self.var_eid,))
                employee_data = cur.fetchone()

                if (employee_data):
                    name, position, contact, email, photo_data = employee_data

                    # Update labels with employee details
                    self.lbl_employee_name.config(text=f"Bem-vindo: {name}")
                    self.lbl_employee_role.config(text=f"Posição: {position}")
                    self.lbl_employee_contact.config(text=f"Contato: {contact}, {email}")

                    # Display the photo
                    self.show_photo(photo_data)

                # Fetch total number of courses and their names
                cur.execute("SELECT COUNT(*), GROUP_CONCAT(name) FROM course WHERE teacher_eid = ?", (self.var_eid,))
                courses_data = cur.fetchone()

                if (courses_data):
                    total_courses, course_names = courses_data

                    # Replace commas with ', ' for better formatting
                    course_names = course_names.replace(',', ', ')

                    # Update labels with course details
                    self.lbl_employee_courses.config(text=f"Total de Cursos: {total_courses}")
                    self.lbl_employee_courses_list.config(text=f"Cursos: {course_names}")

                # Fetch total number of students enrolled in courses taught by the employee
                cur.execute("""
                    SELECT COUNT(DISTINCT roll) 
                    FROM enrollment 
                    WHERE cid IN (SELECT cid FROM course WHERE teacher_eid = ?)
                """, (self.var_eid,))
                total_students = cur.fetchone()[0]

                # Update label with total number of students
                self.lbl_employee_students.config(text=f"Total de Estudantes: {total_students}")
                
                con.close()

                # Schedule the update_employee_details method to be called again after 200 milliseconds
                self.root.after(200, self.update_employee_details)
            except Exception as ex:
                messagebox.showerror("Erro", f"Error fetching data: {str(ex)}")


    def upload_photo(self):
        file_path = filedialog.askopenfilename(title="Selecionar Foto", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])

        if (file_path):
            # Convert the image to base64 to store in the database
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()

            # Update the photo in the database
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            try:
                cur.execute("UPDATE employee SET photo = ? WHERE eid = ?", (encoded_string, self.var_eid))
                con.commit()
                self.show_photo(encoded_string)
                messagebox.showinfo("Successo", "Foto inserida com sucesso!", parent=self.root)
            except Exception as ex:
                messagebox.showerror("Erro", f"Error updating photo: {str(ex)}", parent=self.root)
            finally:
                con.close()


    def show_photo(self, photo_data):
        if (photo_data):
            decoded_data = base64.b64decode(photo_data)

            image = Image.open(io.BytesIO(decoded_data))
            image = image.resize((150, 150), Image.LANCZOS)

            photo = ImageTk.PhotoImage(image)

            self.photo_label.config(image=photo, text="")
            self.photo_label.image = photo
        else:
            self.photo_label.config(image='', text="No Image")


    # =============== Login ===============

    def check_login_status(self):
        if(self.var_eid == None):
            self.logged_in = False
        else:
            self.logged_in = True
            
        if (not self.logged_in):
            self.disable_content()
        else:
            self.enable_content()


    def disable_content(self):
        self.btn_course.config(state=DISABLED)
        self.btn_student.config(state=DISABLED)
        self.btn_enrollment.config(state=DISABLED)
        self.btn_result.config(state=DISABLED)
        self.btn_grade.config(state=DISABLED)
        self.btn_report.config(state=DISABLED)
        self.btn_logout.config(state=DISABLED)
        #self.btn_exit.config(state=DISABLED)

        self.P_Frame.place_forget()


    def enable_content(self):
        self.btn_course.config(state=NORMAL)
        self.btn_student.config(state=NORMAL)
        self.btn_enrollment.config(state=NORMAL)
        self.btn_result.config(state=NORMAL)
        self.btn_grade.config(state=NORMAL)
        self.btn_report.config(state=NORMAL)
        self.btn_logout.config(state=NORMAL)
        #self.btn_exit.config(state=DISABLED)

        self.L_Frame.place_forget()


    def open_login_window(self):
        self.root.destroy()                                 # Destroy the main window
        os.system("python login.py")                        # Run the 'login.py' script to show the login window


def main():
    root = Tk()
    obj = RMS(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()