from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import pandas as pd
import os
import json
import sqlite3
from datetime import datetime
from database_init import populate_database

app = Flask(__name__)
CORS(app)

# @app.after_request
# def add_cors_headers(response):
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#     return response
# Configure paths
db_path = "images"  # Path to the database containing face embeddings
upload_folder = "uploads"  # Folder to temporarily store uploaded images
database_file = "attendance.db"  # SQLite database file

# Ensure upload folder exists
os.makedirs(upload_folder, exist_ok=True)

# Initialize the database
populate_database(database_file)
 
@app.route("/find", methods=["POST"])
def find_faces():
    if "files" not in request.files:
        return jsonify({"error": "No files part in the request"}), 400

    files = request.files.getlist("files")
    course_code = request.form.get("course_code")
    # lesson_time = request.form.get("time")  # Get the lesson start time from the request
    selected_dates = request.form.get('selected_dates')
    dates = []
    if selected_dates:
        dates = json.loads(selected_dates) 

        for date in dates:
            # Example: Insert date into the database along with file info
            print(f"Processing for date: {date}")

    if not files:
        return jsonify({"error": "No files selected"}), 400
    
    if not course_code:
        return jsonify({"error": "Missing course_code parameter"}), 400
    
    if not selected_dates:
        return jsonify({"error": "Missing time parameter"}), 400

    try:
        all_results = []

        for file in files:
            # Save each uploaded file
            file_path = os.path.join(upload_folder, file.filename)
            file.save(file_path)

            # Perform face search using DeepFace
            dfs = DeepFace.find(img_path=file_path, db_path=db_path)
            all_results.append(dfs)

            # Delete the uploaded file after processing
            if os.path.exists(file_path):
                os.remove(file_path)

        # Extract unique student IDs
        students = find_students(all_results)

        # Verify students and record attendance
        record_attendance(students, course_code,dates)

        return jsonify({"students_found": students, "course_code": course_code})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
  

def find_students(dfs):
    merged_df = pd.DataFrame()
    # Merge all DataFrames into one
    if not dfs :
        raise ValueError("No valid data frames found from face recognition.")
    
    for df in dfs:
        for df_ in df:
            merged_df = pd.concat([merged_df, df_])
            if 'identity' not in merged_df.columns:
                raise ValueError("Data frame columns do not contain 'identity'.")
    # Extract unique student IDs
    merged_df['student_id'] = merged_df['identity'].apply(lambda x: os.path.basename(os.path.dirname(x)))
    unique_students = merged_df.drop_duplicates(subset="student_id")["student_id"].tolist()
    # raise ValueError(unique_students)
    return unique_students

def record_attendance(student_ids, course_code, selected_dates):
    """
    Record attendance for the given students in the specified course.
    """

    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()

        course_id = cursor.execute(
            "SELECT id FROM courses WHERE course_code = ?", (course_code,)
        ).fetchone()

        if not course_id:
            raise ValueError(f"Course with code '{course_code}' does not exist.")
        course_id = course_id[0]

        for student_id in student_ids:
            # Check if the student is enrolled in the course
            
            cursor.execute('''
                SELECT * FROM enrollment
                WHERE student_id = ? AND course_id = ?
            ''', (student_id, course_id))
            enrollment = cursor.fetchone()

            if enrollment:
                # Record attendance
                for date in selected_dates:
                    # raise ValueError(date)
                    date = date.split(' ')
                    lesson_date = date[0]
                    lesson_time = date[1]
                    # raise ValueError(date)
                    cursor.execute(

                        """
                        INSERT INTO attendance (student_id, course_id, date, time, status)
                        VALUES (?, ?, ?, ?, 'attended')
                        """,
                        (student_id, course_id, lesson_date, lesson_time)
                    )
            else:
                # Log unidentified or unauthorized student
                print(f"Student {student_id} is not enrolled in course {course_id}")

        conn.commit()

@app.route("/get_attendance", methods=["GET"])
def get_attendance():
    course_code = request.args.get("course_code")
    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()
        
        # Fetch course_id
        course_id = cursor.execute(
            "SELECT id FROM courses WHERE course_code = ?", (course_code,)
        ).fetchone()
        
        if not course_id:
            return jsonify({"error": f"Course with code '{course_code}' not found"}), 400
        
        course_id = course_id[0]
        
        # Fetch all students and attendance status
        query = """
        SELECT s.student_id, a.date, a.time, 
            CASE 
                WHEN a.status = 'attended' THEN '✔'
                WHEN a.status = 'pending' THEN 'p'
                ELSE '✘'
            END AS status
        FROM students s
        LEFT JOIN enrollment e ON s.student_id = e.student_id
        LEFT JOIN attendance a 
          ON a.student_id = s.student_id AND a.course_id = ? 
        WHERE e.course_id = ?
        """
        result = cursor.execute(query, (course_id, course_id)).fetchall()

        # Structure data into a JSON response
        students_data = {}
        for row in result:
            student_id, date, time, status = row
            if student_id not in students_data:
                students_data[student_id] = {"attendance": {}}
            if date and time:
                students_data[student_id]["attendance"][f"{date} {time}"] = status
        
        return jsonify({"students": students_data})

@app.route("/submit_attendance", methods=["POST"])
def submit_attendance():
    data = request.json  # Expect JSON data
    if not data:
        return jsonify({"error": "Missing data"}), 400

    course_code = data.get("course_code")
    attendance_entries = data.get("attendance")  # List of attendance entries

    if not course_code or not attendance_entries:
        return jsonify({"error": "Missing course_code or attendance data"}), 400

    status_map = {
        "✔": "attended",
        "✘": "absent",
        "p": "pending"
    }

    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()

        # Fetch the course ID based on the course_code
        cursor.execute("SELECT id FROM courses WHERE course_code = ?", (course_code,))
        course_id = cursor.fetchone()
        if not course_id:
            return jsonify({"error": "Invalid course_code"}), 400

        course_id = course_id[0]

        # Insert or update attendance data
        for entry in attendance_entries:
            student_id = entry.get("student_id")
            date = entry.get("date")
            time = entry.get("time")
            status_symbol = entry.get("status")

            # Map the frontend status symbol to the backend value
            status = status_map.get(status_symbol)

            if not student_id or not date or not status or not time:
                continue  # Skip invalid entries

            # Check if attendance already exists for this student and date
            cursor.execute("""
                SELECT 1 FROM attendance 
                WHERE student_id = ? AND course_id = ? AND date = ? AND time = ?
            """, (student_id, course_id, date, time))
            exists = cursor.fetchone()

            if exists:
                # Update the existing attendance record
                cursor.execute("""
                    UPDATE attendance 
                    SET status = ? 
                    WHERE student_id = ? AND course_id = ? AND date = ? AND time = ?
                """, (status, student_id, course_id, date, time))
            else:
                # Insert new attendance record
                cursor.execute("""
                    INSERT INTO attendance (student_id, course_id, date, time,status) 
                    VALUES (?, ?, ?, ?, ?)
                """, (student_id, course_id, date, time, status))

        conn.commit()

    return jsonify({"message": "Attendance submitted successfully!"})

@app.route("/register", methods=["POST"])
def register():
    student_id = request.form.get("student_id")
    if not student_id:
        return jsonify({"error": "Missing student_id"}), 400

    if "photos" not in request.files:
        return jsonify({"error": "No photos uploaded"}), 400

    # Create a directory for the student
    student_folder = os.path.join(db_path, student_id)
    os.makedirs(student_folder, exist_ok=True)

    # Save uploaded photos
    files = request.files.getlist("photos")
    saved_files = []
    for file in files:
        if file.filename == "":
            continue

        # Generate a safe file path
        file_path = os.path.join(student_folder, file.filename)
        file.save(file_path)
        saved_files.append(file.filename)

    return jsonify({"message": f"Successfully registered {student_id}.", "saved_files": saved_files}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
