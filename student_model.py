from db import execute_query

def get_all_students():
    query = "SELECT * FROM students"
    return execute_query(query, fetch=True)

def add_student(student_data):
    query = "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)"
    params = (student_data['name'], student_data['age'], student_data['grade'])
    rowcount = execute_query(query, params)
    return rowcount

def get_student_by_id(student_id):
    query = "SELECT * FROM students WHERE id = %s"
    params = (student_id,)
    result = execute_query(query, params, fetch='one')
    return result

def update_student(student_id, name, age, grade):
    query = "UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s"
    params = (name, age, grade, student_id)
    return execute_query(query, params)

def delete_student(student_id):
    query = "DELETE FROM students WHERE id=%s"
    params = (student_id,)
    return execute_query(query, params)


def search_students(query):
    """Search students by name, grade, or ID"""
    search_query = """
    SELECT id, name, age, grade 
    FROM students 
    WHERE name LIKE %s OR grade LIKE %s OR id LIKE %s
    ORDER BY name
    """
    search_term = f"%{query}%"
    params = (search_term, search_term, search_term)
    return execute_query(search_query, params, fetch=True)
