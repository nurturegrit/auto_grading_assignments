import sqlite3

class Connect_DB:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def insert_into_assignments(self, assignment_topic, subject, batch):
        query = '''INSERT INTO assignments (assignment_topic, subject_name, batch_number)
                   VALUES (?, ?, ?)'''
        self.cursor.execute(query, (assignment_topic, subject, batch))
        self.connection.commit()
    
    def get_intern_id(self, email=None, phone=None):
        if phone:
            query = '''
                    SELECT "id" FROM "interns" WHERE "email" = ?
                    '''
            self.cursor.execute(query, phone)
        elif email:
            query = '''
                    SELECT "id" FROM "interns" WHERE "email" = ?
                    '''
            self.cursor.execute(query, email)
        elif email is None and phone is None:
            return None
        intern_id = self.cursor.fetchone()
        return intern_id

    def insert_into_grades(self, assignment_id, score, phone=None, email=None, intern_id=None):
        if phone == email == intern_id:
            return "Input Intern Identifier"
        elif not intern_id:
            intern_id = self.get_intern_id(email, phone)
            
        query = '''INSERT INTO grades (intern_id, assignment_id, score) 
                   VALUES (?, ?, ?)'''
        self.cursor.execute(query, (intern_id, assignment_id, score))
        self.connection.commit()

    def get_assignment_id(self, assignment_topic, subject_name, batch_number):
        query = '''SELECT "assignment_id"
                   FROM "assignments" 
                   WHERE "subject_id" = (
                   SELECT "id"  FROM "subjects" WHERE "subject_name" = ? AND "batch_number" = ?
                   ) AND "assignment_topic" = ?'''
        self.cursor.execute(query, (subject_name, batch_number, assignment_topic))
        assignment_id = self.cursor.fetchone()
        return int(assignment_id)

    def close_connection(self):
        self.connection.close()
