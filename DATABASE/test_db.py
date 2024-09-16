import pytest
import sqlite3
from DataBase import Connect_DB


# Fixture to create a temporary database for testing
@pytest.fixture
def setup_db():
    db_file = "test.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create schema for testing
    cursor.executescript(
        """
        DROP TABLE IF EXISTS grades;
        DROP TABLE IF EXISTS assignments;
        DROP TABLE IF EXISTS subjects;
        DROP TABLE IF EXISTS mentors;
        DROP TABLE IF EXISTS interns;
        DROP TABLE IF EXISTS batches;
        CREATE TABLE batches (
            batch_number INTEGER PRIMARY KEY,
            start_date NUMERIC NOT NULL,
            end_date NUMERIC
        );

        CREATE TABLE interns (
            id INTEGER PRIMARY KEY,
            type TEXT CHECK(type IN ('Full Time', 'Part Time')),
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            date_of_birth NUMERIC,
            gender TEXT CHECK(gender IN ('Male', 'Female', 'Other', NULL)),
            batch_number INTEGER NOT NULL,
            FOREIGN KEY (batch_number) REFERENCES batches(batch_number)
        );

        CREATE TABLE mentors (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE
        );

        CREATE TABLE subjects (
            id INTEGER PRIMARY KEY,
            batch_number INTEGER NOT NULL,
            subject_name TEXT NOT NULL,
            mentor_id INTEGER NOT NULL,
            FOREIGN KEY (batch_number) REFERENCES batches(batch_number),
            FOREIGN KEY (mentor_id) REFERENCES mentors(id)
        );

        CREATE TABLE assignments (
            id INTEGER PRIMARY KEY,
            subject_id INTEGER NOT NULL,
            assignment_topic TEXT NOT NULL,
            total_score INTEGER,
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        );

        CREATE TABLE grades (
            intern_id INTEGER NOT NULL,
            assignment_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            PRIMARY KEY (intern_id, assignment_id),
            FOREIGN KEY (intern_id) REFERENCES interns(id),
            FOREIGN KEY (assignment_id) REFERENCES assignments(id)
        );
    """
    )

    # Insert some initial data for testing
    cursor.executescript(
        """
        INSERT INTO batches (batch_number, start_date, end_date) 
        VALUES (13, '2023-09-01', '2024-09-01');

        INSERT INTO interns (id, type, first_name, last_name, email, phone, date_of_birth, gender, batch_number) 
        VALUES (1, 'Full Time', 'Ritwicka', 'Majumder', 'ritwicka.majumder7@gmail.com', '1234567890', '2003-05-07', 'Female', 13);

        INSERT INTO mentors (id, first_name, last_name, email, phone) 
        VALUES (1, 'John', 'Smith', 'john.smith@example.com', '1231231234');

        INSERT INTO subjects (id, batch_number, subject_name, mentor_id) 
        VALUES (1, 13, 'Python', 1);

        INSERT INTO assignments (id, subject_id, assignment_topic, total_score) 
        VALUES (1, 1, 'Python Basics', 100);
    """
    )

    conn.commit()
    conn.close()

    yield db_file



# Test cases
def test_get_assignment_id(setup_db):
    db = Connect_DB(setup_db)
    assignment_id = db.get_assignment_id("Python Basics", "Python", 13)
    assert assignment_id == 1, "Assignment ID should be 1"


def test_get_intern_id(setup_db):
    db = Connect_DB(setup_db)
    intern_id = db.get_intern_id(email="ritwicka.majumder7@gmail.com")
    assert intern_id == 1, "Intern ID should be 1"


def test_insert_into_grades(setup_db):
    db = Connect_DB(setup_db)
    db.insert_into_grades(
        90,
        intern_email="ritwicka.majumder7@gmail.com",
        assignment_topic="Python Basics",
        subject_name="Python",
        batch_number=13,
    )

    # Verify insertion
    db.cursor.execute("SELECT * FROM grades WHERE intern_id = 1 AND assignment_id = 1")
    grade = db.cursor.fetchone()
    assert grade == (1, 1, 90), "Grade should be inserted with score 90"


def test_close_connection(setup_db):
    db = Connect_DB(setup_db)
    db.close_connection()
    with pytest.raises(sqlite3.ProgrammingError):
        db.cursor.execute(
            "SELECT * FROM grades"
        )  # Should raise error since connection is closed


# if __name__ == "__main__":
#     setup_db()
#     test_get_intern_id('test.db')
#     test_get_assignment_id('test.db')
#     test_insert_into_grades('test.db')

