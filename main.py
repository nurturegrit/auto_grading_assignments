from backend.chatgpt_api import HomeworkGrader
from database.DataBase import Connect_DB
from backend.mail import send_feedback, extract_marks_and_feedback
from backend.getinput import GetInputs
import sys, csv, os


def main():
    # ------------- Taking Input and config files------------------------------ #
    assignment_directory = os.path.join('Input', sys.argv[1])
    inputs = GetInputs(assignment_directory)
    
    #------------- Connect with database ---------------------- #
    db_path = os.path.join('database', 'grader.db')
    db = Connect_DB(db_path)


    
    #------------------ Grading --------------------------------- #
    with open('Keys/key.txt') as file:
        token = file.readline().strip()
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o-mini"
    output_tokens = 200
    
    # Initialize Grader
    autograder = HomeworkGrader(token, endpoint, model_name, output_tokens)
    # Dict for storing grades
    grades_by_interns = {}
    total_score = 0
    for question_id in inputs.questions:
            total_score += 100
            question = inputs.questions[question_id]
            # for each question, select corresponding solution by interns
            for intern_id in inputs.solutions:
                 answer = inputs.solutions[intern_id][question_id]
                 response = autograder.grade_answer(question, answer)

                 grade, feedback = extract_marks_and_feedback(response)
                 grades_by_interns[intern_id] = grades_by_interns.get(intern_id, 0) + int(grade)


    #--------------------- Storing Grades in Database ------------------ #
    #---------------------- Send Feedback ------------------------------ #




