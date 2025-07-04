from db import get_connection

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")  # Make sure table exists
    students = cursor.fetchall()
    conn.close()
    return students

def add_student(data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)"
    cursor.execute(sql, (data['name'], data['age'], data['grade']))
    conn.commit()
    conn.close()


def get_student_by_id(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def update_student(student_id, name, age, grade):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s",
                   (name, age, grade, student_id))
    conn.commit()
    conn.close()
    return {"message": "Student updated successfully"}

def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    conn.close()
    return {"message": "Student deleted successfully"}

