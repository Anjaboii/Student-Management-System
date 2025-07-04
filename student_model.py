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
