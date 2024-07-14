from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

class ReportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Relatórios - Result Management System")
        self.root.geometry("1200x730")
        self.root.config(bg="white")
        self.root.focus_force()

        # =============== Title ===============
        title = Label(self.root, 
                      text="Gerenciar Relatórios", 
                      font=("goudy old style", 20, "bold"), 
                      bg="orange", 
                      fg="#262626")
        title.place(x=10, y=15, width=1180, height=35)

        # =============== Variables ===============
        self.var_search_course = StringVar()
        self.var_search_student = StringVar()
        self.var_grade_type = StringVar()
        self.var_plot_type = StringVar()

        self.grade_type_list = ['Trabalhos', 'Participação', 'Testes', 'Provas', 'Total']
        self.grade_type_map = {
            'Trabalhos': 'homework_grade',
            'Participação': 'participation_grade',
            'Testes': 'midterm_grade',
            'Provas': 'final_exam_grade',
            'Total': 'total_grade'
        }

        self.plot_type_list = ['Bar', 'Line', 'Scatter', 'Pie', 'Histogram']

        self.course_list = []
        self.fetch_course()

        self.student_list = []
        self.fetch_student()

        # =============== Search ===============
        lbl_search_course = Label(self.root, text="Curso:", font=("goudy old style", 15, "bold"), bg="white")
        lbl_search_course.place(x=50, y=70)
        self.txt_search_course = ttk.Combobox(self.root, textvariable=self.var_search_course, values=self.course_list, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_search_course.place(x=120, y=70, width=150)
        self.txt_search_course.set("Select")
        self.btn_search_course = Button(self.root, text="Pesquisar", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.search_course)
        self.btn_search_course.place(x=290, y=70, width=100, height=29)

        lbl_search_student = Label(self.root, text="Estudante:", font=("goudy old style", 15, "bold"), bg="white")
        lbl_search_student.place(x=420, y=70)
        self.txt_search_student = ttk.Combobox(self.root, textvariable=self.var_search_student, values=self.student_list, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_search_student.place(x=520, y=70, width=150)
        self.txt_search_student.set("Select")
        self.btn_search = Button(self.root, text="Pesquisar", font=("goudy old style", 15, "bold"), bg="green", fg="white", cursor="hand2", command=self.search_student)
        self.btn_search.place(x=690, y=70, width=100, height=29)
        
        self.btn_clear = Button(self.root, text="Limpar", font=("goudy old style", 15, "bold"), bg="gray", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=820, y=70, width=100, height=30)

         # =============== Separator ===============

        self.h_separator = ttk.Separator(self.root, orient="horizontal")
        self.h_separator.place(x=40, y=120, relwidth=0.93)

        # =============== Main Frame ===============
        self.main_frame = Frame(self.root, bg="white", highlightthickness=1, highlightbackground="black")
        self.main_frame.place(x=50, y=145, width=1100, height=550)

        # --------------- Left Frame ---------------
        self.left_frame = Frame(self.main_frame, bg="lightgray")
        self.left_frame.place(relwidth=0.3, relheight=1)

        self.border_frame = Frame(self.left_frame, bg="black", width=1)
        self.border_frame.place(relx=0.997, rely=0, relwidth=0.001, relheight=1)
        self.border_frame.place_forget()

        # --------------- Right Frame ---------------
        self.right_frame = Frame(self.main_frame, bg="lightgray")
        self.right_frame.place(relx=0.3, relwidth=0.7, relheight=1)

        self.lbl_plot_type = Label(self.right_frame, text="Gráfico:", font=("goudy old style", 15, "bold"), bg="white")
        self.lbl_plot_type.place(x=40, y=10)
        self.txt_plot_type = ttk.Combobox(self.right_frame, textvariable=self.var_plot_type, values=self.plot_type_list, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_plot_type.place(x=130, y=10, width=200)
        self.txt_plot_type.set("Select")

        self.lbl_grade_type = Label(self.right_frame, text="Nota:", font=("goudy old style", 15, "bold"), bg="white")
        self.lbl_grade_type.place(x=350, y=10)
        self.txt_grade_type = ttk.Combobox(self.right_frame, textvariable=self.var_grade_type, values=self.grade_type_list, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_grade_type.place(x=450, y=10, width=150)
        self.txt_grade_type.set("Select")

        self.btn_plot_course = Button(self.right_frame, text="Plotar", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.plot_course_grades)
        self.btn_plot_course.place(x=630, y=10, width=100, height=29)
        self.btn_plot_student = Button(self.right_frame, text="Plotar", font=("goudy old style", 15, "bold"), bg="green", fg="white", cursor="hand2", command=self.plot_student_grades)
        self.btn_plot_student.place(x=630, y=10, width=100, height=29)

        # --------------- Plot Frame ---------------
        self.plot_frame = Frame(self.right_frame, bg="lightgray")
        self.plot_frame.place(x=0, y=50, width=825, height=500)

        # Initially hide plot options
        self.hide_plot_options()


    # ==================== Search Courses ====================

    def fetch_course(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()

            if (len(rows) > 0):
                for row in rows:
                    self.course_list.append(row[0])
            
            con.close()
        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    def search_course(self):
        subject = self.var_search_course.get()

        if (not subject or subject == "Select"):
            messagebox.showwarning("Input Error", "Selecione um curso")
            return

        # Clear the previous elements in the frames if there are any
        self.hide_plot_options()
        self.clean_plot_frame()
        self.clean_course_details()
        self.clean_student_details()
        self.border_frame.place_forget()
        self.var_search_student.set("Select")
        self.var_grade_type.set("Select")
        self.var_plot_type.set("Select")

        # Makes the 'left frame' right border appear
        self.border_frame.place(relx=0.997, rely=0, relwidth=0.001, relheight=1)

        # Makes the elements in the 'right frame' bar appear
        self.show_plot_options()
        self.btn_plot_course.place(x=600, y=10, width=100, height=29)

        # Change the 'right frame' and 'plot frame' background change from gray to white 
        self.right_frame.config(bg="white")
        self.plot_frame.config(bg="white")

        # Shows the details of the course in question
        self.display_course_details(subject)


    def plot_course_grades(self):
        # Get selected options from the dropdown menus
        subject = self.var_search_course.get()
        grade_type = self.var_grade_type.get()
        plot_type = self.var_plot_type.get()

        # Check if subject, grade type, and plot type are selected
        if (not subject or subject == "Select"):
            messagebox.showwarning("Input Error", "Subjeto selecionado invalido")
            return

        if (grade_type not in self.grade_type_list):
            messagebox.showwarning("Input Error", "Tipo de nota inválido")
            return

        if (plot_type not in self.plot_type_list):
            messagebox.showwarning("Input Error", "Tipo de gráfico Inválido")
            return

        # Retrieve the corresponding column name for the selected grade type
        grade_column = self.grade_type_map[grade_type]

        # Connect to the database and execute SQL query to fetch data
        conn = sqlite3.connect('rms.db')
        c = conn.cursor()
        c.execute(f"SELECT student_name, {grade_column} FROM result WHERE course_name = ?", (subject,))
        rows = c.fetchall()

        # Check if there is no data for the selected subject and grade type
        if (not rows):
            messagebox.showinfo("No Data", f"No {grade_type} found for the subject")
            return

        # Sort rows by grades in ascending order
        rows.sort(key=lambda x: x[1])

        # Extract student names and grades from the fetched data
        student_names = [row[0] for row in rows]
        grades = [int(row[1]) for row in rows]  # Convert grades to integers

        # Create a new matplotlib figure and axis
        fig, ax = plt.subplots(figsize=(10, 5))

        # Plot based on the selected plot type
        if (plot_type == 'Bar'):
            ax.bar(student_names, grades)
            ax.set_xlabel('Estudantes')
            ax.set_ylabel('Notas')
            ax.set_title(f'{grade_type} para {subject}')
            ax.set_xticklabels(student_names, rotation=45)
            ax.set_ylim(0, 100)  # Set y-axis limits to range from 0 to 100
            ax.grid(True)

        elif (plot_type == 'Line'):
            ax.plot(student_names, grades, marker='o')
            ax.set_xlabel('Estudantes')
            ax.set_ylabel('Notas')
            ax.set_title(f'{grade_type} para {subject}')
            ax.set_xticklabels(student_names, rotation=45)
            ax.set_ylim(0, 100)  # Set y-axis limits to range from 0 to 100
            ax.grid(True)

        elif (plot_type == 'Scatter'):
            ax.scatter(student_names, grades)
            ax.set_xlabel('Estudantes')
            ax.set_ylabel('Notas')
            ax.set_title(f'{grade_type} para {subject}')
            ax.set_xticklabels(student_names, rotation=45)
            ax.set_ylim(0, 100)  # Set y-axis limits to range from 0 to 100
            ax.grid(True)

        elif (plot_type == 'Pie'):
            # Count the frequency of each grade value
            grade_counts = Counter(grades)
            
            # Get unique grade values and their corresponding frequencies
            unique_grades = list(grade_counts.keys())
            grade_frequencies = list(grade_counts.values())
            
            # Create the pie chart
            ax.pie(grade_frequencies, labels=unique_grades, autopct='%1.1f%%', startangle=140)
            ax.axis('equal')
            plt.title(f'{grade_type} distribuição para {subject}')

        elif (plot_type == 'Histogram'):
            # Create a histogram of the grades
            ax.hist(grades, bins=10, edgecolor='black')
            ax.set_xlabel('Notas')
            ax.set_ylabel('Frequencia')
            ax.set_title(f'{grade_type} distribuição para {subject}')
            ax.grid(True)

        else:
            messagebox.showwarning("Plot Error", "Tipo de grafico selecionado é inválido")
            return

        # Clear any existing plot in the plot frame
        for widget in self.plot_frame.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()

        # Display the plot in the plot frame
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=0, width=825, height=500)

        # Close the database connection
        conn.close()


    def fetch_student_count(self, course_name):
        conn = sqlite3.connect('rms.db')
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM enrollment WHERE course_name = ?", (course_name,))
        count = c.fetchone()[0]

        conn.close()
        return count


    def fetch_grade_averages(self, course_name):

        conn = sqlite3.connect('rms.db')
        c = conn.cursor()
        averages = {}

        for grade_type in self.grade_type_map.values():
            c.execute(f"SELECT AVG({grade_type}) FROM result WHERE course_name = ?", (course_name,))
            averages[grade_type] = c.fetchone()[0]
        
        conn.close()
        return averages


    def display_course_details(self, course_name):

        for widget in self.left_frame.winfo_children():
            if (isinstance(widget, Label) and widget != self.lbl_plot_type):
                widget.destroy()

        total_students = self.fetch_student_count(course_name)
        grade_averages = self.fetch_grade_averages(course_name)

        y_position = 10
        Label(self.left_frame, text=f"Cursos: {course_name}", font=("goudy old style", 15, "bold"), bg="lightgray").place(x=10, y=y_position)
        y_position += 30
        Label(self.left_frame, text=f"Total de Estudantes: {total_students}", font=("goudy old style", 15, "bold"), bg="lightgray").place(x=10, y=y_position)
        y_position += 30

        for grade_type in self.grade_type_list:
            grade_column = self.grade_type_map[grade_type]
            average_grade = grade_averages.get(grade_column, 0)
            Label(self.left_frame, text=f"{grade_type} (Avg): {average_grade:.2f}", font=("goudy old style", 15, "bold"), bg="lightgray").place(x=10, y=y_position)
            y_position += 30

    # ==================== Search Student ====================

    def fetch_student(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT name FROM student")
            rows = cur.fetchall()

            if (len(rows) > 0):
                for row in rows:
                    self.student_list.append(row[0])
            
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


    def search_student(self):
        student_name = self.var_search_student.get()

        if (not student_name or student_name == "Select"):
            messagebox.showwarning("Input Error", "É necessário selecionar um estudante")
            return

        # Clear the previous elements in the frames if there are any
        self.hide_plot_options()
        self.clean_plot_frame()
        self.clean_student_details()
        self.var_search_course.set("Select")
        self.var_grade_type.set("Select")
        self.var_plot_type.set("Select")

        # Makes the 'left frame' right border appear
        self.border_frame.place(relx=0.997, rely=0, relwidth=0.001, relheight=1)

        # Makes the elements in the 'right frame' bar appear
        self.show_plot_options()
        self.btn_plot_student.place(x=600, y=10, width=100, height=29)

        # Change the 'right frame' and 'plot frame' background change from gray to white 
        self.right_frame.config(bg="white")
        self.plot_frame.config(bg="white")

        # Shows the details of the student in question
        self.display_student_details(student_name)


    def plot_student_grades(self):
        # Get selected options from the dropdown menus
        student_name = self.var_search_student.get()
        grade_type = self.var_grade_type.get()
        plot_type = self.var_plot_type.get()

        # Check if student, grade type, and plot type are selected
        if (not student_name or student_name == "Select"):
            messagebox.showwarning("Input Error", "É necessário selecionar um estudante")
            return

        if (grade_type not in self.grade_type_list):
            messagebox.showwarning("Input Error", "Tipo de nota inválida")
            return

        if (plot_type not in self.plot_type_list):
            messagebox.showwarning("Input Error", "Tipo de gráfico inválido")
            return

        # Retrieve the corresponding column name for the selected grade type
        grade_column = self.grade_type_map[grade_type]

        # Connect to the database and execute SQL query to fetch data
        conn = sqlite3.connect('rms.db')
        c = conn.cursor()
        c.execute(f"SELECT course_name, {grade_column} FROM result WHERE student_name = ?", (student_name,))
        rows = c.fetchall()

        # Check if there is no data for the selected student and grade type
        if (not rows):
            messagebox.showinfo("No Data", f"No {grade_type} found for the student")
            return

        # Sort rows by grades in ascending order
        rows.sort(key=lambda x: x[1])

        # Extract course names and grades from the fetched data
        course_names = [row[0] for row in rows]
        grades = [int(row[1]) for row in rows]  # Convert grades to integers

        # Create a new matplotlib figure and axis
        fig, ax = plt.subplots(figsize=(10, 5))

        # Plot based on the selected plot type
        if (plot_type == 'Bar'):
            ax.bar(course_names, grades)
            ax.set_xlabel('Cursos')
            ax.set_ylabel('Notas')
            ax.set_title(f'{grade_type} para {student_name}')
            ax.set_xticklabels(course_names, rotation=45)
            ax.set_ylim(0, 100)  # Set y-axis limits to range from 0 to 100
            ax.grid(True)

        elif (plot_type == 'Line'):
            ax.plot(course_names, grades, marker='o')
            ax.set_xlabel('Cursos')
            ax.set_ylabel('Notas')
            ax.set_title(f'{grade_type} para {student_name}')
            ax.set_xticklabels(course_names, rotation=45)
            ax.set_ylim(0, 100)  # Set y-axis limits to range from 0 to 100
            ax.grid(True)

        elif (plot_type == 'Scatter'):
            ax.scatter(course_names, grades)
            ax.set_xlabel('Cursos')
            ax.set_ylabel('Notas')
            ax.set_title(f'{grade_type} para {student_name}')
            ax.set_xticklabels(course_names, rotation=45)
            ax.set_ylim(0, 100)  # Set y-axis limits to range from 0 to 100
            ax.grid(True)

        elif (plot_type == 'Pie'):
            # Count the frequency of each grade value
            grade_counts = Counter(grades)
            
            # Get unique grade values and their corresponding frequencies
            unique_grades = list(grade_counts.keys())
            grade_frequencies = list(grade_counts.values())
            
            # Create the pie chart
            ax.pie(grade_frequencies, labels=unique_grades, autopct='%1.1f%%', startangle=140)
            ax.axis('equal')
            plt.title(f'{grade_type} distribuição para {student_name}')

        elif (plot_type == 'Histogram'):
            # Create a histogram of the grades
            ax.hist(grades, bins=10, edgecolor='black')
            ax.set_xlabel('Notas')
            ax.set_ylabel('Frequencia')
            ax.set_title(f'{grade_type} distribuição para {student_name}')
            ax.grid(True)

        else:
            messagebox.showwarning("Plot Error", "Tipo de gráfico inválido")
            return

        # Clear any existing plot in the plot frame
        for widget in self.plot_frame.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()

        # Display the plot in the plot frame
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=0, width=825, height=500)

        # Close the database connection
        conn.close()


    def fetch_student_enrollment(self, student_name):
        conn = sqlite3.connect('rms.db')
        c = conn.cursor()

        c.execute("SELECT course_name FROM enrollment WHERE student_name = ?", (student_name,))
        courses = c.fetchall()

        conn.close()
        return [course[0] for course in courses]


    def fetch_student_grades(self, student_name):
        conn = sqlite3.connect('rms.db')
        c = conn.cursor()
        grades = {}

        for grade_type in self.grade_type_map.values():
            c.execute(f"SELECT AVG({grade_type}) FROM result WHERE student_name = ?", (student_name,))
            grades[grade_type] = c.fetchone()[0]

        conn.close()
        return grades


    def display_student_details(self, student_name):

        for widget in self.left_frame.winfo_children():
            if (isinstance(widget, Label) and widget != self.lbl_plot_type):
                widget.destroy()

        enrolled_courses = self.fetch_student_enrollment(student_name)
        grade_averages = self.fetch_student_grades(student_name)

        y_position = 10
        Label(self.left_frame, text=f"Estudante: {student_name}", font=("goudy old style", 15, "bold"), bg="lightgray").place(x=10, y=y_position)
        y_position += 30
        Label(self.left_frame, text=f"Total de Cursos: {len(enrolled_courses)}", font=("goudy old style", 15, "bold"), bg="lightgray").place(x=10, y=y_position)
        y_position += 30

        courses_text = ", ".join(enrolled_courses[::-1])
        Label(self.left_frame, text=f"Cursos: {courses_text}", font=("goudy old style", 15, "bold"), bg="lightgray").place(x=10, y=y_position)
        y_position += 30

        for grade_type in self.grade_type_list:
            grade_column = self.grade_type_map[grade_type]
            average_grade = grade_averages.get(grade_column, 0)
            Label(self.left_frame, text=f"{grade_type} (Avg): {average_grade:.2f}", font=("goudy old style", 15, "bold"), bg="lightgray").place(x=10, y=y_position)
            y_position += 30


    # ==================== Other Methods ====================

    def hide_plot_options(self):
        self.lbl_plot_type.place_forget()
        self.txt_plot_type.place_forget()
        self.btn_plot_course.place_forget()
        self.btn_plot_student.place_forget()

        self.lbl_grade_type.place_forget()
        self.txt_grade_type.place_forget()

    def show_plot_options(self):
        self.lbl_grade_type.place(x=10, y=10)
        self.txt_grade_type.place(x=80, y=10, width=200)

        self.lbl_plot_type.place(x=320, y=10)
        self.txt_plot_type.place(x=410, y=10, width=150)


    def clean_plot_frame(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

    def clean_course_details(self):
        for widget in self.left_frame.winfo_children():
            if isinstance(widget, Label) and widget != self.lbl_plot_type:
                widget.destroy()

    def clean_student_details(self):
        for widget in self.left_frame.winfo_children():
            if widget.winfo_class() == 'Label' and widget != self.lbl_plot_type:
                widget.destroy()


    def clear(self):
        self.var_search_course.set("Select")
        self.var_search_student.set("Select")
        self.var_grade_type.set("Select")
        self.var_plot_type.set("Select")

        self.hide_plot_options()
        self.clean_plot_frame()
        self.clean_course_details()
        self.clean_student_details()
        self.border_frame.place_forget()

        self.right_frame.config(bg="lightgray")
        self.plot_frame.config(bg="lightgray")


if __name__ == "__main__":
    root = Tk()
    obj = ReportClass(root)
    root.mainloop()