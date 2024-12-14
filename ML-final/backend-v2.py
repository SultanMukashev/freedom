from flask import Flask, request, jsonify
from deepface import DeepFace
import pandas as pd
import os
import sqlite3
from datetime import datetime
from database_init import populate_database

app = Flask(__name__)

# Configure paths
db_path = "images-2"  # Path to the database containing face embeddings
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
    lesson_time = request.form.get("time")  # Get the lesson start time from the request
    if not files:
        return jsonify({"error": "No files selected"}), 400
    
    if not course_code:
        return jsonify({"error": "Missing course_code parameter"}), 400
    
    if not lesson_time:
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
        record_attendance(students, course_code,lesson_time)

        return jsonify({"students_found": students, "course_code": course_code})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def find_students(dfs):
    merged_df = pd.DataFrame()
    # Merge all DataFrames into one
    for df in dfs:
        for df_ in df:
            merged_df = pd.concat([merged_df, df_])
    # Extract unique student IDs
    merged_df['student_id'] = merged_df['identity'].apply(lambda x: os.path.basename(os.path.dirname(x)))
    unique_students = merged_df.drop_duplicates(subset="student_id")["student_id"].tolist()
    return unique_students

def record_attendance(student_ids, course_code, lesson_time):
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
                cursor.execute(
                    """
                    INSERT INTO attendance (student_id, course_id, date, time, status)
                    VALUES (?, ?, DATE('now'), ?, 'attended')
                    """,
                    (student_id, course_id, lesson_time)
                )
            else:
                # Log unidentified or unauthorized student
                print(f"Student {student_id} is not enrolled in course {course_id}")

        conn.commit()

if __name__ == "__main__":
    app.run(debug=True)
