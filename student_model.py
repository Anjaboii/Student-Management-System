from db import execute_query

def get_all_students():
    """Get all students ordered by name"""
    query = """
    SELECT id, name, age, grade, created_at, updated_at 
    FROM students 
    ORDER BY name ASC
    """
    return execute_query(query, fetch='all')

def get_student_by_id(student_id):
    """Get student by ID"""
    query = """
    SELECT id, name, age, grade, created_at, updated_at 
    FROM students 
    WHERE id = %s
    """
    return execute_query(query, params=(student_id,), fetch='one')

def add_student(data):
    """Add a new student"""
    # Validate required fields
    required_fields = ['name', 'age', 'grade']
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate age
    age = int(data['age'])
    if age < 1 or age > 150:
        raise ValueError("Age must be between 1 and 150")
    
    # Validate name length
    name = str(data['name']).strip()
    if len(name) < 1 or len(name) > 100:
        raise ValueError("Name must be between 1 and 100 characters")
    
    # Validate grade length
    grade = str(data['grade']).strip()
    if len(grade) < 1 or len(grade) > 50:
        raise ValueError("Grade must be between 1 and 50 characters")
    
    query = """
    INSERT INTO students (name, age, grade) 
    VALUES (%s, %s, %s)
    """
    
    rows_affected = execute_query(query, params=(name, age, grade))
    
    if rows_affected > 0:
        return {"success": True, "message": "Student added successfully"}
    else:
        raise Exception("Failed to add student")

def update_student(student_id, name, age, grade):
    """Update student information"""
    # Validate inputs
    if not student_id or student_id < 1:
        raise ValueError("Invalid student ID")
    
    age = int(age)
    if age < 1 or age > 150:
        raise ValueError("Age must be between 1 and 150")
    
    name = str(name).strip()
    if len(name) < 1 or len(name) > 100:
        raise ValueError("Name must be between 1 and 100 characters")
    
    grade = str(grade).strip()
    if len(grade) < 1 or len(grade) > 50:
        raise ValueError("Grade must be between 1 and 50 characters")
    
    # Check if student exists
    existing_student = get_student_by_id(student_id)
    if not existing_student:
        raise ValueError("Student not found")
    
    query = """
    UPDATE students 
    SET name = %s, age = %s, grade = %s, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s
    """
    
    rows_affected = execute_query(query, params=(name, age, grade, student_id))
    
    if rows_affected > 0:
        return {"success": True, "message": "Student updated successfully"}
    else:
        raise Exception("Failed to update student")

def delete_student(student_id):
    """Delete a student"""
    # Validate student ID
    if not student_id or student_id < 1:
        raise ValueError("Invalid student ID")
    
    # Check if student exists
    existing_student = get_student_by_id(student_id)
    if not existing_student:
        raise ValueError("Student not found")
    
    query = "DELETE FROM students WHERE id = %s"
    rows_affected = execute_query(query, params=(student_id,))
    
    if rows_affected > 0:
        return {"success": True, "message": "Student deleted successfully"}
    else:
        raise Exception("Failed to delete student")

def get_students_by_grade(grade):
    """Get all students in a specific grade"""
    query = """
    SELECT id, name, age, grade, created_at, updated_at 
    FROM students 
    WHERE grade = %s 
    ORDER BY name ASC
    """
    return execute_query(query, params=(grade,), fetch='all')

def get_student_count():
    """Get total number of students"""
    query = "SELECT COUNT(*) as count FROM students"
    result = execute_query(query, fetch='one')
    return result['count'] if result else 0

def get_grade_statistics():
    """Get statistics by grade"""
    query = """
    SELECT grade, COUNT(*) as count, AVG(age) as avg_age 
    FROM students 
    GROUP BY grade 
    ORDER BY grade ASC
    """
    return execute_query(query, fetch='all')

def search_students(search_term):
    """Search students by name or grade"""
    if not search_term:
        return get_all_students()
    
    search_term = f"%{search_term}%"
    query = """
    SELECT id, name, age, grade, created_at, updated_at 
    FROM students 
    WHERE name LIKE %s OR grade LIKE %s 
    ORDER BY name ASC
    """
    return execute_query(query, params=(search_term, search_term), fetch='all')