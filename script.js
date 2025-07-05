// Use your local Flask backend URL here
const API_BASE_URL = 'https://studentmanagement-1.up.railway.app/api';
let editingStudentId = null;
let searchTimeout = null;

// Load students when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadStudents();
    setupSearch();
});

// Setup search functionality
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length === 0) {
            loadStudents();
            hideSearchInfo();
            return;
        }
        
        searchTimeout = setTimeout(() => {
            searchStudents(query);
        }, 300);
    });
    
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const query = this.value.trim();
            if (query.length > 0) {
                searchStudents(query);
            }
        }
    });
}

function searchStudents(query) {
    fetch(`${API_BASE_URL}/students/search?q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage('Search error: ' + data.error, 'error');
            return;
        }
        displayStudents(data.students);
        showSearchInfo(data.total, data.query);
    })
    .catch(error => {
        showMessage('Error searching students: ' + error.message, 'error');
    });
}

function showSearchInfo(total, query) {
    const searchInfo = document.getElementById('searchInfo');
    searchInfo.style.display = 'block';
    searchInfo.innerHTML = `Found <strong>${total}</strong> student${total !== 1 ? 's' : ''} matching "<strong>${query}</strong>"`;
}

function hideSearchInfo() {
    const searchInfo = document.getElementById('searchInfo');
    searchInfo.style.display = 'none';
}

function clearSearch() {
    document.getElementById('searchInput').value = '';
    hideSearchInfo();
    loadStudents();
}

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

function addStudent(studentData) {
    fetch(`${API_BASE_URL}/students`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(studentData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage('Error adding student: ' + data.error, 'error');
            return;
        }
        showMessage('Student added successfully!', 'success');
        clearForm();
        const searchQuery = document.getElementById('searchInput').value.trim();
        if (searchQuery) {
            searchStudents(searchQuery);
        } else {
            loadStudents();
        }
    })
    .catch(error => {
        showMessage('Error adding student: ' + error.message, 'error');
    });
}

function loadStudents() {
    fetch(`${API_BASE_URL}/students`)
    .then(response => response.json())
    .then(students => {
        displayStudents(students);
    })
    .catch(error => {
        showMessage('Error loading students: ' + error.message, 'error');
        document.getElementById('studentsContainer').innerHTML = '<div class="error">Failed to load students</div>';
    });
}

function displayStudents(students) {
    const container = document.getElementById('studentsContainer');
    
    if (!students || students.length === 0) {
        const searchQuery = document.getElementById('searchInput').value.trim();
        const emptyMessage = searchQuery ? 
            `<div class="empty-state"><h3>No students found</h3><p>No students match your search for "<strong>${searchQuery}</strong>"</p><button class="btn" onclick="clearSearch()">Show All Students</button></div>` :
            `<div class="empty-state"><h3>No students found</h3><p>Add your first student using the form above!</p></div>`;
        container.innerHTML = emptyMessage;
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

function editStudent(id) {
    fetch(`${API_BASE_URL}/students/${id}`)
    .then(response => response.json())
    .then(student => {
        if (student.error) {
            showMessage('Error loading student: ' + student.error, 'error');
            return;
        }
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

function updateStudent(id, studentData) {
    fetch(`${API_BASE_URL}/students/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(studentData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage('Error updating student: ' + data.error, 'error');
            return;
        }
        showMessage('Student updated successfully!', 'success');
        clearForm();
        const searchQuery = document.getElementById('searchInput').value.trim();
        if (searchQuery) {
            searchStudents(searchQuery);
        } else {
            loadStudents();
        }
    })
    .catch(error => {
        showMessage('Error updating student: ' + error.message, 'error');
    });
}

function deleteStudent(id) {
    if (confirm('Are you sure you want to delete this student?')) {
        fetch(`${API_BASE_URL}/students/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showMessage('Error deleting student: ' + data.error, 'error');
                return;
            }
            showMessage('Student deleted successfully!', 'success');
            const searchQuery = document.getElementById('searchInput').value.trim();
            if (searchQuery) {
                searchStudents(searchQuery);
            } else {
                loadStudents();
            }
        })
        .catch(error => {
            showMessage('Error deleting student: ' + error.message, 'error');
        });
    }
}

function clearForm() {
    document.getElementById('studentForm').reset();
    editingStudentId = null;
    document.querySelector('.form-section h2').textContent = 'Add New Student';
    document.querySelector('button[type="submit"]').textContent = 'Add Student';
}

function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = `<div class="message ${type}">${message}</div>`;
    
    setTimeout(() => {
        messageDiv.innerHTML = '';
    }, 3000);
}
