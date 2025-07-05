from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from db import get_connection
from student_model import (
    get_all_students, 
    add_student, 
    get_student_by_id, 
    update_student, 
    delete_student
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Enable CORS for all routes
CORS(app)

# ==================== HTML ROUTES ====================

@app.route('/')
def index():
    """Home page - Dashboard"""
    try:
        # Get total students count
        students = get_all_students()
        total_students = len(students)
        
        # Get students by grade
        grade_stats = {}
        for student in students:
            grade = student['grade']
            grade_stats[grade] = grade_stats.get(grade, 0) + 1
        
        # Get recent students (last 5)
        recent_students = students[-5:] if len(students) >= 5 else students
        
        return render_template('dashboard.html', 
                             total_students=total_students,
                             grade_stats=list(grade_stats.items()),
                             recent_students=recent_students)
    
    except Exception as e:
        flash(f'Database error: {e}', 'error')
        return render_template('error.html')

@app.route('/students')
def students():
    """List all students"""
    try:
        students_data = get_all_students()
        return render_template('students.html', students=students_data)
    
    except Exception as e:
        flash(f'Database error: {e}', 'error')
        return render_template('error.html')

@app.route('/student/<int:student_id>')
def student_detail(student_id):
    """View student details"""
    try:
        student = get_student_by_id(student_id)
        
        if not student:
            flash('Student not found!', 'error')
            return redirect(url_for('students'))
        
        return render_template('student_detail.html', student=student)
    
    except Exception as e:
        flash(f'Database error: {e}', 'error')
        return render_template('error.html')

@app.route('/student/add', methods=['GET', 'POST'])
def add_student_route():
    """Add new student"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        grade = request.form.get('grade', '').strip()
        
        # Validation
        if not name or not age or not grade:
            flash('All fields are required!', 'error')
            return render_template('add_student.html')
        
        try:
            age = int(age)
            if age < 1 or age > 100:
                flash('Age must be between 1 and 100!', 'error')
                return render_template('add_student.html')
        except ValueError:
            flash('Age must be a valid number!', 'error')
            return render_template('add_student.html')
        
        try:
            student_data = {
                'name': name,
                'age': age,
                'grade': grade
            }
            add_student(student_data)
            flash('Student added successfully!', 'success')
            return redirect(url_for('students'))
        
        except Exception as e:
            flash(f'Database error: {e}', 'error')
            return render_template('add_student.html')
    
    return render_template('add_student.html')

@app.route('/student/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student_route(student_id):
    """Edit student"""
    try:
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            age = request.form.get('age', '').strip()
            grade = request.form.get('grade', '').strip()
            
            # Validation
            if not name or not age or not grade:
                flash('All fields are required!', 'error')
                return redirect(url_for('edit_student_route', student_id=student_id))
            
            try:
                age = int(age)
                if age < 1 or age > 100:
                    flash('Age must be between 1 and 100!', 'error')
                    return redirect(url_for('edit_student_route', student_id=student_id))
            except ValueError:
                flash('Age must be a valid number!', 'error')
                return redirect(url_for('edit_student_route', student_id=student_id))
            
            update_student(student_id, name, age, grade)
            flash('Student updated successfully!', 'success')
            return redirect(url_for('student_detail', student_id=student_id))
        
        # GET request - show edit form
        student = get_student_by_id(student_id)
        if not student:
            flash('Student not found!', 'error')
            return redirect(url_for('students'))
        
        return render_template('edit_student.html', student=student)
    
    except Exception as e:
        flash(f'Database error: {e}', 'error')
        return render_template('error.html')

@app.route('/student/delete/<int:student_id>')
def delete_student_route(student_id):
    """Delete student"""
    try:
        # Check if student exists
        student = get_student_by_id(student_id)
        if not student:
            flash('Student not found!', 'error')
            return redirect(url_for('students'))
        
        delete_student(student_id)
        flash('Student deleted successfully!', 'success')
        return redirect(url_for('students'))
    
    except Exception as e:
        flash(f'Database error: {e}', 'error')
        return redirect(url_for('students'))

# ==================== API ROUTES ====================

@app.route('/api/students', methods=['GET'])
def api_get_students():
    """API: Get all students"""
    try:
        students_data = get_all_students()
        return jsonify(students_data)
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/students', methods=['POST'])
def api_add_student():
    """API: Add new student"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
        
        name = data.get('name', '').strip()
        age = data.get('age')
        grade = data.get('grade', '').strip()
        
        # Validation
        if not name or not age or not grade:
            return jsonify({
                'error': 'All fields (name, age, grade) are required'
            }), 400
        
        try:
            age = int(age)
            if age < 1 or age > 100:
                return jsonify({
                    'error': 'Age must be between 1 and 100'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Age must be a valid number'
            }), 400
        
        student_data = {
            'name': name,
            'age': age,
            'grade': grade
        }
        
        student_id = add_student(student_data)
        
        return jsonify({
            'message': 'Student added successfully',
            'student_id': student_id
        }), 201
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    """API: Get student by ID"""
    try:
        student = get_student_by_id(student_id)
        
        if not student:
            return jsonify({
                'error': 'Student not found'
            }), 404
        
        return jsonify(student)
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def api_update_student(student_id):
    """API: Update student"""
    try:
        # Check if student exists
        student = get_student_by_id(student_id)
        if not student:
            return jsonify({
                'error': 'Student not found'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
        
        name = data.get('name', '').strip()
        age = data.get('age')
        grade = data.get('grade', '').strip()
        
        # Validation
        if not name or not age or not grade:
            return jsonify({
                'error': 'All fields (name, age, grade) are required'
            }), 400
        
        try:
            age = int(age)
            if age < 1 or age > 100:
                return jsonify({
                    'error': 'Age must be between 1 and 100'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Age must be a valid number'
            }), 400
        
        update_student(student_id, name, age, grade)
        
        return jsonify({
            'message': 'Student updated successfully'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    """API: Delete student"""
    try:
        # Check if student exists
        student = get_student_by_id(student_id)
        if not student:
            return jsonify({
                'error': 'Student not found'
            }), 404
        
        delete_student(student_id)
        
        return jsonify({
            'message': 'Student deleted successfully'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/students/search', methods=['GET'])
def api_search_students():
    """API: Search students"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({
                'error': 'Search query is required'
            }), 400
        
        # Get all students and filter
        all_students = get_all_students()
        
        # Simple search by name or grade
        matching_students = []
        for student in all_students:
            if (query.lower() in student['name'].lower() or 
                query.lower() in student['grade'].lower()):
                matching_students.append(student)
        
        return jsonify({
            'students': matching_students,
            'total': len(matching_students),
            'query': query
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({
            'error': 'API endpoint not found'
        }), 404
    return render_template('error.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    if request.path.startswith('/api/'):
        return jsonify({
            'error': 'Internal server error'
        }), 500
    return render_template('error.html'), 500

if __name__ == '__main__':
    # Development server
    app.run(
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true',
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )