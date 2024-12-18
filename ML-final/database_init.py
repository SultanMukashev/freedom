import sqlite3

# Database file
database_file = "attendance.db"

def populate_database(database_file):
    # List of student IDs
    student_ids = [
        "220101097", "220103070", "220107003", "220107016", "220107028", "220107032", "220107034", 
        "220107048", "220107049", "220107068", "220107075", "220107077", "220107086", "220107092", 
        "220107094", "220107104", "220107116", "220107122", "220107125", "190107071", "190107111", 
        "200107065", "220107005", "220107007", "220107010", "220107012", "220107027", "220107035", 
        "220107043", "220107056", "220107076", "220107079", "220107102", "220107103", "220107110", 
        "220107114", "220107129", "220107131", "220107135", "220107145", "220107148", "220107149", 
        "220107151", "220107157", "220107158", "220107006", "220107008", "220107014", "220107020", 
        "220107026", "220107037", "220107038", "220107051", "220107060", "220107065", "220107069", 
        "220107072", "220107085", "220107088", "220107093", "220107097", "220107108", "220107118", 
        "220107127", "220107139", "220107142", "220107152", "220107156"
    ]

    # Course information
    course_code = "CSS324"
    course_name = "Machine Learning"

    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()

        # Create tables
        # cursor.execute("DROP TABLE ATTENDANCE")
        # cursor.execute("DROP TABLE students")
        # cursor.execute("DROP TABLE enrollment")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT UNIQUE NOT NULL,
                course_name TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                course_id INTEGER NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(student_id),
                FOREIGN KEY(course_id) REFERENCES courses(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                course_id INTEGER NOT NULL,
                date DATE NOT NULL,
                time TIME NOT NULL,
                status TEXT DEFAULT NULL,
                FOREIGN KEY(student_id) REFERENCES students(student_id),
                FOREIGN KEY(course_id) REFERENCES courses(id)
            )
        ''')

        # Insert the course into the courses table

        cursor.execute(
            "INSERT OR IGNORE INTO courses (course_code, course_name) VALUES (?, ?)",
            (course_code, course_name)
        )

        # Get the course_id for the inserted course
        course_id = cursor.execute(
            "SELECT id FROM courses WHERE course_code = ?", (course_code,)
        ).fetchone()[0]

        # Insert students into the students table
        for student_id in student_ids:
            cursor.execute(
                "INSERT OR IGNORE INTO students (student_id) VALUES (?)",
                (student_id,)
            )

        # Enroll all students into the course
        for student_id in student_ids:
            cursor.execute(
                "INSERT OR IGNORE INTO enrollment (student_id, course_id) VALUES (?, ?)",
                (student_id, course_id)
            )

        conn.commit()

if __name__ == "__main__":
    populate_database(database_file)
    print("Database populated successfully!")
