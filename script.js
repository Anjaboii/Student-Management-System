
        const API_BASE_URL = 'http://localhost:5000';
        let editingStudentId = null;

        // Load students when page loads
        document.addEventListener('DOMContentLoaded', function() {
            loadStudents();
        });

        // Handle form submission
        document.getElementById('studentForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('name').value;
            const age = parseInt(document.getElementById('age').value);
            const grade = document.getElementById('grade').value;

            if (editingStudentId) {
                updateStudent(editingStudentId, { name, age, grade });
            } else {
                addStudent({ name, age, grade });
            }
        });

        // Add new student
        function addStudent(studentData) {
            fetch(`${API_BASE_URL}/students`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(studentData)
            })
            .then(response => response.json())
            .then(data => {
                showMessage('Student added successfully!', 'success');
                clearForm();
                loadStudents();
            })
            .catch(error => {
                showMessage('Error adding student: ' + error.message, 'error');
            });
        }

        // Load all students
        function loadStudents() {
            fetch(`${API_BASE_URL}/students`)
            .then(response => response.json())
            .then(students => {
                displayStudents(students);
            })
            .catch(error => {
                showMessage('Error loading students: ' + error.message, 'error');
                document.getElementById('studentsContainer').innerHTML = 
                    '<div class="error">Failed to load students</div>';
            });
        }

        // Display students
        function displayStudents(students) {
            const container = document.getElementById('studentsContainer');
            
            if (students.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <h3>No students found</h3>
                        <p>Add your first student using the form above!</p>
                    </div>
                `;
                return;
            }

            const studentsHTML = students.map(student => `
                <div class="student-card">
                
                    <div class="student-name">${student.name}</div>
                    <strong>ID:</strong> ${student.id}<br>
                    <div class="student-info">
                        <strong>Age:</strong> ${student.age} years<br>
                        <strong>Grade:</strong> ${student.grade}
                    </div>
                    <div class="student-actions">
                        <button class="btn btn-small" onclick="editStudent(${student.id})">Edit</button>
                        <button class="btn btn-danger btn-small" onclick="deleteStudent(${student.id})">Delete</button>
                    </div>
                </div>
            `).join('');

            container.innerHTML = `<div class="students-grid">${studentsHTML}</div>`;
        }

        // Edit student
        function editStudent(id) {
            fetch(`${API_BASE_URL}/students/${id}`)
            .then(response => response.json())
            .then(student => {
                document.getElementById('name').value = student.name;
                document.getElementById('age').value = student.age;
                document.getElementById('grade').value = student.grade;
                
                editingStudentId = id;
                document.querySelector('.form-section h2').textContent = 'Edit Student';
                document.querySelector('button[type="submit"]').textContent = 'Update Student';
            })
            .catch(error => {
                showMessage('Error loading student: ' + error.message, 'error');
            });
        }

        // Update student
        function updateStudent(id, studentData) {
            fetch(`${API_BASE_URL}/students/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(studentData)
            })
            .then(response => response.json())
            .then(data => {
                showMessage('Student updated successfully!', 'success');
                clearForm();
                loadStudents();
            })
            .catch(error => {
                showMessage('Error updating student: ' + error.message, 'error');
            });
        }

        // Delete student
        function deleteStudent(id) {
            if (confirm('Are you sure you want to delete this student?')) {
                fetch(`${API_BASE_URL}/students/${id}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    showMessage('Student deleted successfully!', 'success');
                    loadStudents();
                })
                .catch(error => {
                    showMessage('Error deleting student: ' + error.message, 'error');
                });
            }
        }

        // Clear form
        function clearForm() {
            document.getElementById('studentForm').reset();
            editingStudentId = null;
            document.querySelector('.form-section h2').textContent = 'Add New Student';
            document.querySelector('button[type="submit"]').textContent = 'Add Student';
        }

        // Show message
        function showMessage(message, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.innerHTML = `<div class="message ${type}">${message}</div>`;
            
            // Clear message after 3 seconds
            setTimeout(() => {
                messageDiv.innerHTML = '';
            }, 3000);
        }
