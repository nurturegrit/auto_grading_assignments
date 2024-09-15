from backend.chatgpt_api import HomeworkGrader
from database.class_db import Connect_DB
from backend.mail import send_feedback, extract_marks_and_feedback
from backend.getinput import GetInputs



def main():
    # ------------- Taking Input ------------------------------ #
    assignment_directory = ''

    inputs = GetInputs(assignment_directory)
    
    #------------------ Grading --------------------------------- #
    with open('Keys/key.txt') as file:
        token = file.readline().strip()
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o-mini"
    output_tokens = 200
    
    # Initialize Grader
    autograder = HomeworkGrader(token, endpoint, model_name, output_tokens)
    # Dict for storing grades

    for question_id in inputs.questions:
            question = inputs.questions[question_id]
            # for each question, select corresponding solution by interns
            for intern_id in inputs.solutions:
                 answer = inputs.solutions[intern_id][question_id]
                 response = autograder.grade_answer(question, answer)

                 grade, feedback = extract_marks_and_feedback(response)

                 



    #--------------------- Storing Grades in Database ------------------ #
    #---------------------- Send Feedback ------------------------------ #




