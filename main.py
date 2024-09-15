from backend.chatgpt_api import HomeworkGrader
from database.DataBase import Connect_DB
from backend.mail import send_feedback, extract_marks_and_feedback
from backend.getinput import GetInputs
import sys, json, os

def main():
    # ------------- Config files------------------------------ #
    config_path = os.path.join('Keys', 'autograder_config.json')
    with open(config_path) as file:
         config = json.load(file)
         if config is None:
           sys.exit("AutoGrader Not Configured")
         from_email_address = config['email']
         password = config['password']
         smtp_address = config['smtp']
         
         
    assignment_directory = os.path.join('Input', sys.argv[1])
    config_path = os.path.join(assignment_directory, 'config.json')
    with open(config_path) as file:
        config = json.load(file)
        if config is None:
           sys.exit("No Config File For Assignment Directory")
        assignment_topic = config['assignment_topic']
        total_score = int(config['total_score'])
        subject_name = config['subject_name']
        batch_number = int(config['batch_number'])
            
    #----------------------- Taking Input --------------------------- #
    inputs = GetInputs(assignment_directory)
    
    #------------- Connect with database ---------------------- #
    db_path = os.path.join('database', 'grader.db')
    db = Connect_DB(db_path)

    # Insert the new assignment in the Database
    subject_id = db.get_subject_id(subject_name, batch_number)
    db.insert_into_assignments(subject_id, assignment_topic, total_score)
    # Get Assignment ID for storing scores
    assignment_id = db.get_assignment_id(assignment_topic=assignment_topic, subject=subject_name, batch=batch_number)

    
    #------------------ Grading --------------------------------- #
    with open('Keys/key.txt') as file:
        token = file.readline().strip()
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o-mini"
    output_tokens = 200
    
    # Initialize Grader
    autograder = HomeworkGrader(token, endpoint, model_name, output_tokens)
    # Dict for storing grades
    grades_by_intern_id = {}
    feedback_by_email = {}
    per_score = 0
    for question_id in inputs.questions:
             # question_score = inputs.questions[question_id]['full_score']
             question_score = 100
             per_score += question_score
             question = inputs.questions[question_id]
             # for each question, select corresponding solution by interns
             for intern_id in inputs.solutions:
                 try:
                    answer = inputs.solutions[intern_id][question_id]
                    response = autograder.grade_answer(question, answer, question_score)

                    grade, feedback = extract_marks_and_feedback(response)
                    grades_by_intern_id[intern_id] = grades_by_intern_id.get(intern_id, 0) + int(grade)

                    intern_email = db.get_intern_email(intern_id)
                    feedback_by_email[intern_email] = feedback_by_email.get[intern_email, ''] + '\n' + feedback
                 except Exception as e:
                     print('FOR INTERN: ' + intern_id, 'QUESTION_ID: ' + question_id)
                     print(e)

    #--------------------- Storing Grades in Database ------------------ #
    # Normalizing Grades
    factor = per_score/total_score
    for intern_id in grades_by_intern_id:
        grades_by_intern_id[intern_id] *= factor
    
    for intern_id in grades_by_intern_id:
        score = grades_by_intern_id[intern_id]
        db.insert_into_grades(score, intern_id=intern_id, assignment_id=assignment_id)

    #---------------------- Send Feedback ------------------------------ #
    subject = f'Assessment Feedback For Assignment {assignment_topic}.'

    for email in feedback_by_email:
        feedback = feedback_by_email[email]
        send_feedback(smtp_address=smtp_address, to_email=email, subject=subject, feedback_message=feedback, from_email=from_email_address, from_password=password)


if __name__ == "__main__":
    main()