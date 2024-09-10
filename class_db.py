import sqlite3

class Connect_DB:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def insert_into_batches(self, batch_number, start_date, end_date):
        query = '''INSERT INTO batches (batch_number, start_date, end_date) 
                   VALUES (?, ?, ?)'''
        self.cursor.execute(query, (batch_number, start_date, end_date))
        self.connection.commit()

    def insert_into_interns(self, intern_id, intern_type, first_name, last_name, email, phone, date_of_birth, gender, batch_number):
        query = '''INSERT INTO interns (id, type, first_name, last_name, email, phone, date_of_birth, gender, batch_number) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        self.cursor.execute(query, (intern_id, intern_type, first_name, last_name, email, phone, date_of_birth, gender, batch_number))
        self.connection.commit()

    def insert_into_instructors(self, first_name, last_name, email, phone):
        query = '''INSERT INTO instructors (first_name, last_name, email, phone) 
                   VALUES (?, ?, ?, ?)'''
        self.cursor.execute(query, first_name, last_name, email, phone))
        self.connection.commit()

    def insert_into_subjects(self, batch_number, subject_name, instructor_first_name, instructor_last_name):
        instructor_id = self.get_instructor_id(first_name, last_name)
        query = '''INSERT INTO batch_subjects (batch_id, subject_name, instructor_id) 
                   VALUES (?, ?, ?)'''
        self.cursor.execute(query, (batch_number, subject_name, instructor_id))
        self.connection.commit()

    def insert_into_passion_project(self, project_id, name, project_type, head_instructor, guide_instructor1=None, guide_instructor2=None):
        query = '''INSERT INTO passion_project (id, name, type, head_instructor, guide_instructor1, guide_instructor2) 
                   VALUES (?, ?, ?, ?, ?, ?)'''
        self.cursor.execute(query, (project_id, name, project_type, head_instructor, guide_instructor1, guide_instructor2))
        self.connection.commit()

    def insert_into_assignments(self, assignment_id, subject_id, assignment_topic, total_score, instructor_id):
        query = '''INSERT INTO assignments (id, subject_id, assignment_topic, total_score, instructor_id) 
                   VALUES (?, ?, ?, ?, ?)'''
        self.cursor.execute(query, (assignment_id, subject_id, assignment_topic, total_score, instructor_id))
        self.connection.commit()

    def insert_into_grades(self, intern_id, assignment_id, teacher_id, score, date):
        query = '''INSERT INTO grades (intern_id, assignment_id, teacher_id, score, date) 
                   VALUES (?, ?, ?, ?, ?)'''
        self.cursor.execute(query, (intern_id, assignment_id, teacher_id, score, date))
        self.connection.commit()

    def insert_into_batch_subject(self, batch_id, subject_id):
        query = '''INSERT INTO batch_subject (batch_id, subject_id) 
                   VALUES (?, ?)'''
        self.cursor.execute(query, (batch_id, subject_id))
        self.connection.commit()

    def insert_into_batch_instructor(self, batch_id, instructor_id):
        query = '''INSERT INTO batch_instructor (batch_id, instructor_id) 
                   VALUES (?, ?)'''
        self.cursor.execute(query, (batch_id, instructor_id))
        self.connection.commit()

    def create_indexes(self):
        queries = [
            '''CREATE INDEX IF NOT EXISTS idx_interns_batch_number ON interns (batch_number)''',
            '''CREATE INDEX IF NOT EXISTS idx_grades_intern_id ON grades (intern_id)''',
            '''CREATE INDEX IF NOT EXISTS idx_grades_assignment_id ON grades (assignment_id)''',
            '''CREATE INDEX IF NOT EXISTS idx_assignments_subject_id ON assignments (subject_id)''',
            '''CREATE INDEX IF NOT EXISTS idx_subjects_instructor_id ON subjects (instructor_id)''',
            '''CREATE INDEX IF NOT EXISTS idx_student_performance_instructor_id ON grades (teacher_id)''',
            '''CREATE INDEX IF NOT EXISTS idx_student_performance_subject_name ON subjects (subject_name)''',
            '''CREATE INDEX IF NOT EXISTS idx_batch_subject_batch_id ON batch_subject (batch_id)''',
            '''CREATE INDEX IF NOT EXISTS idx_batch_instructor_batch_id ON batch_instructor (batch_id)'''
        ]
        for query in queries:
            self.cursor.execute(query)
        self.connection.commit()

    def create_views(self):
        queries = [
            '''CREATE VIEW IF NOT EXISTS average_intern_scores AS
               SELECT 
                   i.id AS intern_id,
                   i.first_name,
                   i.last_name,
                   i.batch_number,
                   AVG(g.score) AS average_score
               FROM 
                   interns i
               JOIN 
                   grades g ON i.id = g.intern_id
               GROUP BY 
                   i.id, i.first_name, i.last_name, i.batch_number''',
            '''CREATE VIEW IF NOT EXISTS student_performance AS
               SELECT 
                   i.id AS student_id,
                   i.first_name,
                   i.last_name,
                   s.subject_name,
                   g.score,
                   g.teacher_id,
                   g.assignment_id
               FROM 
                   interns i
               JOIN 
                   grades g ON i.id = g.intern_id
               JOIN 
                   assignments a ON g.assignment_id = a.id
               JOIN 
                   subjects s ON a.subject_id = s.id'''
        ]
        for query in queries:
            self.cursor.execute(query)
        self.connection.commit()

    def query_average_scores_per_batch(self, batch_number):
        query = '''SELECT intern_id, first_name, last_name, average_score
                   FROM average_intern_scores
                   WHERE batch_number = ?'''
        self.cursor.execute(query, (batch_number,))
        return self.cursor.fetchall()

    def get_instructor_id(self, first_name, last_name):
        self.cursor.execute(''' SELECT id FROM instructors WHERE first_name = ? AND last_name = ?)

    def query_student_performance(self, instructor_id, subject_name):
        query = '''SELECT student_id, first_name, last_name, subject_name, AVG(score) AS average_score
                   FROM student_performance
                   WHERE teacher_id = ? AND subject_name = ?
                   GROUP BY student_id, first_name, last_name, subject_name'''
        self.cursor.execute(query, (instructor_id, subject_name))
        return self.cursor.fetchall()


    def close_connection(self):
        self.connection.close()
