import sqlite3

def create_db():
    con = sqlite3.connect(database="rms.db")                        # Connects to the SQLite database or create it if it doesn't exist
    cur = con.cursor()                                              # Creates a cursor object to execute SQL queries

    # Create the 'course' table if it doesn't exist
    cur.execute("CREATE TABLE IF NOT EXISTS course(cid INTEGER PRIMARY KEY AUTOINCREMENT, name text, duration text, charges text, teacher_name text, teacher_eid text, description text)")
    con.commit()                                                    # Commits the changes to the database

    # Create the 'student' table if it doesn't exist
    cur.execute("CREATE TABLE IF NOT EXISTS student(roll INTEGER PRIMARY KEY AUTOINCREMENT, name text, email text, gender text, dob text, contact text, admission text, state text, city text, pin text, address text)")
    con.commit()                                                    # Commits the changes to the database

    # Create the 'enrollment' table if it doesn't exist
    cur.execute("CREATE TABLE IF NOT EXISTS enrollment(enr_id INTEGER PRIMARY KEY AUTOINCREMENT, roll INTEGER, student_name text, cid INTEGER, course_name text, course_description text)")
    con.commit()  

    # Create the 'result' table if it doesn't exist
    cur.execute("CREATE TABLE IF NOT EXISTS result(rid INTEGER PRIMARY KEY AUTOINCREMENT, enr_id text, roll text, student_name text, cid text, course_name text, homework_grade text, participation_grade text, midterm_grade text, final_exam_grade text, total_grade text)")
    con.commit()                                                    # Commits the changes to the database

    # Create the 'employee' table if it doesn't exist
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT, name text, adress text, contact text, email text, question text, answer text, password text, position text, photo TEXT)")
    con.commit()                                                    # Commits the changes to the database

    # Create the 'employee' table if it doesn't exist
    cur.execute("CREATE TABLE IF NOT EXISTS assignments(assign_id INTEGER PRIMARY KEY AUTOINCREMENT, eid text, e_name text, e_position text, cid text, course_name text)")
    con.commit()                                                    # Commits the changes to the database

    # Close the database connection
    con.close()
    

# Call the 'create_db' function to initialize the database
create_db()