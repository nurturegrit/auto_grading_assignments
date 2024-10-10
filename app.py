from flask import Flask, render_template, session, request, redirect, flash, url_for
import os, json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/teacher_login')
def teacher_login():
    return render_template('teacher_login.html')

@app.route('/teacher_dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    # Sample data retrieval logic
    flash("Welcome to the Teacher Dashboard!", "info")
    return render_template('teacher_dashboard.html')

@app.route('/create_assignment', methods=['GET', 'POST'])
def create_assignment():
    if request.method == 'POST':
        assignment_name = request.form['assignment_name']
        subject = request.form['subject']
        total_marks = request.form['total_marks']
        start_date = request.form['start_date']
        deadline_date = request.form['deadline_date']
        batch_number = request.form.get('batch_number')
        questions = request.form.getlist('questions')

        if not assignment_name or any(not q for q in questions):
            flash("Please fill out all fields.", "danger")
            return redirect(url_for('create_assignment'))

        assignment_folder = f"Input/{assignment_name.replace(' ', '_')}"
        os.makedirs(f"{assignment_folder}/Questions", exist_ok=True)

        config = {
            "assignment_topic": assignment_name,
            "total_score": total_marks,
            "subject_name": subject,
            "batch_number": batch_number,
            "start_date": start_date,
            "deadline_date": deadline_date
        }

        with open(f"{assignment_folder}/config.json", 'w') as config_file:
            json.dump(config, config_file, indent=4)

        for i, question in enumerate(questions, start=1):
            with open(f"{assignment_folder}/Questions/{i}.txt", 'w') as f:
                f.write(question)

        os.system(f'python add_assignment.py {assignment_name}')
        
        flash("Assignment created successfully!", "success")
        return redirect('/teacher_dashboard')

    return render_template('create_assignment.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_name = request.form['student_name']
        
        if not student_name:
            flash("Please enter your name.", "danger")
            return redirect(url_for('student_login'))
        
        session['student_name'] = student_name
        flash(f"Welcome, {student_name}!", "success")
        return redirect('/student_dashboard')
        
    return render_template('student_login.html')

@app.route('/student_dashboard', methods=['GET', 'POST'])
def student_dashboard():
    assignments = [d for d in os.listdir('Input') if os.path.isdir(os.path.join('Input', d))]
    return render_template('student_dashboard.html', assignments=assignments)

@app.route('/view_assignment/<assignment_name>')
def view_assignment(assignment_name):
    questions = []
    assignment_path = os.path.join("Input", assignment_name, "Questions")

    if os.path.exists(assignment_path):
        question_files = sorted(os.listdir(assignment_path))
        for question_file in question_files:
            with open(os.path.join(assignment_path, question_file)) as f:
                questions.append(f.read())
                
    return render_template('view_assignment.html', assignment_name=assignment_name, questions=questions, student_name=session.get('student_name'))

@app.route('/upload_solution/<assignment_name>/<question_number>', methods=['POST'])
def upload_solution(assignment_name, question_number):
    student_name = session.get('student_name')
    solution = request.files['solution']
    
    if student_name and solution:
        filename = secure_filename(f"{question_number}.py")
        student_folder_path = os.path.join('Input', assignment_name, student_name)
        os.makedirs(student_folder_path, exist_ok=True)
        solution.save(os.path.join(student_folder_path, filename))
        flash("Solution uploaded successfully!", "success")
        
    return redirect(url_for('view_assignment', assignment_name=assignment_name))

if __name__ == '__main__':
    app.run(debug=True)