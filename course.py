from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Cursos - Sistema de Gestão de Resultados")
        self.root.geometry("1200x480")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(False, False)

        # =============== Title ===============
        title = Label(self.root, text="Gerenciar Cursos", font=("goudy old style",20,"bold"), bg="#033054", fg="white")
        title.place(x=10, y=15, width=1180, height=35)

        # =============== Variables ===============
        self.var_course_id = StringVar()
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_teacher_eid = StringVar()
        self.var_teacher_name = StringVar()

        self.teacher_list = []
        self.teacher_map = {}  # Dictionary to store teacher name to eid mapping
        self.fetch_teacher()

        # =============== Labels ===============
        lbl_courseName = Label(self.root, text="Nome do Curso", font=("goudy old style", 15, "bold"), bg="white")
        lbl_courseName.place(x=10, y=60)
        lbl_duration = Label(self.root, text="Duração", font=("goudy old style", 15, "bold"), bg="white")
        lbl_duration.place(x=10, y=100)
        lbl_charges = Label(self.root, text="Vagas", font=("goudy old style", 15, "bold"), bg="white")
        lbl_charges.place(x=10, y=140)
        lbl_teacher = Label(self.root, text="Professor", font=("goudy old style", 15, "bold"), bg="white")
        lbl_teacher.place(x=10, y=180)
        lbl_description = Label(self.root, text="Descrição", font=("goudy old style", 15, "bold"), bg="white")
        lbl_description.place(x=10, y=220)

        self.lbl_teacher_id = Label(self.root, text="Professor ID: ", font=("goudy old style", 15, "bold"), bg="white")
        self.lbl_teacher_id.place(x=370, y=180)
        self.lbl_teacher_id.place_forget()

        # --------------- Entry Fields ---------------
        self.txt_courseName = Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_courseName.place(x=150, y=60, width=200)
        txt_duration = Entry(self.root, textvariable=self.var_duration, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_duration.place(x=150, y=100, width=200)
        txt_charges = Entry(self.root, textvariable=self.var_charges, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_charges.place(x=150, y=140, width=200)

        self.txt_teacher = ttk.Combobox(self.root, textvariable=self.var_teacher_name, values=self.teacher_list, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_teacher.place(x=150, y=180, width=200)
        self.txt_teacher.set("Select")
        self.txt_teacher.bind("<<ComboboxSelected>>", self.update_teacher_eid)  # Bind event to update teacher eid

        self.txt_description = Text(self.root, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_description.place(x=150, y=220, width=500, height=130)

        # --------------- Buttons ---------------
        self.btn_add = Button(self.root, text="Salvar", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.add)
        self.btn_add.place(x=150, y=400, width=110, height=40)
        self.btn_update = Button(self.root, text="Atualizar", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=270, y=400, width=110, height=40)
        self.btn_delete = Button(self.root, text="Deletar", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=390, y=400, width=110, height=40)
        self.btn_clear = Button(self.root, text="Limpar", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=510, y=400, width=110, height=40)

        # --------------- Search Panel ---------------
        self.var_search = StringVar()

        lbl_search_courseName = Label(self.root, text="Nome do Curso", font=("goudy old style", 15, "bold"), bg="white")
        lbl_search_courseName.place(x=720, y=60)
        txt_search_courseName = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_search_courseName.place(x=870, y=60, width=180)
        self.btn_search = Button(self.root, text="Pesquisar", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.search)
        self.btn_search.place(x=1070, y=60, width=120, height=28)

        # --------------- Course Table Widget ---------------
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        scroll_y = Scrollbar(self.C_Frame, orient=VERTICAL)
        scroll_x = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.CourseTable = ttk.Treeview(self.C_Frame, columns=("cid", "name", "duration", "charges", "teacher_name", "teacher_eid", "description"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.CourseTable.xview)
        scroll_y.config(command=self.CourseTable.yview)

        self.CourseTable.heading("cid", text="ID do Curso")
        self.CourseTable.heading("name", text="Nome")
        self.CourseTable.heading("duration", text="Duração")
        self.CourseTable.heading("charges", text="Vagas")
        self.CourseTable.heading("teacher_name", text="Professor")
        self.CourseTable.heading("teacher_eid", text="Teacher ID")
        self.CourseTable.heading("description", text="Descrição")

        self.CourseTable["show"] = 'headings'
        self.CourseTable.column("cid", width=100)
        self.CourseTable.column("name", width=100)
        self.CourseTable.column("duration", width=100)
        self.CourseTable.column("charges", width=100)
        self.CourseTable.column("teacher_name", width=100)
        self.CourseTable.column("teacher_eid", width=0, stretch=NO)
        self.CourseTable.column("description", width=150)

        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()


    # Adds the names of teachers from the database to the 'teacher_list' variable and maps their IDs
    def fetch_teacher(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT eid, name FROM employee WHERE position=?", ("Teacher",))
            rows = cur.fetchall()

            if (len(rows)>0):
                for row in rows:
                    self.teacher_list.append(row[1])
                    self.teacher_map[row[1]] = row[0]  # Map teacher name to eid
            
            con.close()

        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    # Updates the teacher eid when a teacher is selected from the combobox
    def update_teacher_eid(self, event):
        selected_teacher = self.var_teacher_name.get()
        teacher_id = self.teacher_map.get(selected_teacher, "")
        self.var_teacher_eid.set(teacher_id)

        self.lbl_teacher_id.config(text=f"Professor ID: {teacher_id}")


    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    def get_data(self, ev):
        self.txt_courseName.config(state="readonly")

        r = self.CourseTable.focus()
        content = self.CourseTable.item(r)
        row = content["values"]

        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.var_teacher_name.set(row[4])
        
        #self.var_teacher_eid.set(row[5])
        self.var_teacher_eid.set(self.teacher_map.get(row[4], ""))
        self.lbl_teacher_id.config(text=f"Professor ID: {self.var_teacher_eid.get()}")

        self.txt_description.delete('1.0', END)
        self.txt_description.insert(END, row[6])


    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            if self.var_course.get() == "":
                messagebox.showerror("Erro", "Nome do curso é necessário", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Nome do curso já existe", parent=self.root)
                else:
                    cur.execute("INSERT INTO course (name, duration, charges, teacher_name, teacher_eid, description) VALUES (?,?,?,?,?,?)", (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.var_teacher_name.get(),
                        self.var_teacher_eid.get(),
                        self.txt_description.get("1.0", END)
                    ))
                    con.commit()
                    messagebox.showinfo("Sucesso", "Curso adicionado com sucesso", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            if self.var_course.get() == "":
                messagebox.showerror("Erro", "Nome do curso é necessário", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Erro", "Seleciona curso da lista", parent=self.root)
                else:
                    cur.execute("UPDATE course SET duration=?, charges=?, teacher_name=?, teacher_eid=?, description=? WHERE name=?", (
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.var_teacher_name.get(),
                        self.var_teacher_eid.get(),
                        self.txt_description.get("1.0", END),
                        self.var_course.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Sucesso", "Curso atualizado com sucesso", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            if self.var_course.get() == "":
                messagebox.showerror("Erro", "Nome do curso é necessario", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Erro", "Primeiro seleciona um curso da lista", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirmar", "Você realmente quer deletar?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM course WHERE name=?", (self.var_course.get(),))
                        con.commit()
                        messagebox.showinfo("Deletar", "Curso deletado com sucesso", parent=self.root)
                        self.show()

        except Exception as ex:
            messagebox.showerror("Erro", f"Error due to {str(ex)}")


    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_teacher_name.set("")
        self.var_teacher_eid.set("")
        self.txt_description.delete('1.0', END)
        self.txt_courseName.config(state=NORMAL)
        self.var_search.set("")

        self.teacher_list.clear()                                           # Clear the course list
        self.txt_teacher.set("Select")                                      # Reset the combobox to the default value
        
        self.lbl_teacher_id.config(text="Professor ID: ")


    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM course WHERE name LIKE ?", ('%'+self.var_search.get()+'%',))
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()
