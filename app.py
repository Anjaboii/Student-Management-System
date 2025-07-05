from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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

@app.route('/api/students')
def api_students():
    """API endpoint for students data"""
    try:
        students_data = get_all_students()
        return jsonify({
            'success': True,
            'data': students_data,
            'count': len(students_data)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html'), 500

if __name__ == '__main__':
    # Development server
    app.run(
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true',
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )