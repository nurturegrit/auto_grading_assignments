import sqlite3

class Connect_DB:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def insert_into_grades(self, intern_id, assignment_id, score):
        query = '''INSERT INTO grades (intern_id, assignment_id, score) 
                   VALUES (?, ?, ?)'''
        self.cursor.execute(query, (intern_id, assignment_id, score))
        self.connection.commit()

    def assignment_id(self, assignment_topic, subject_name, batch_number):
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
