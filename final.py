import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI

class HomeworkGrader:
    def __init__(self, token, endpoint, model_name, assignment):
        self.client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )
        self.model_name = model_name
        self.assignment = assignment

    def grade_answer(self, answer):
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a master at python algorithms and data structures.",
                },
                {
                    "role": "user",
                    "content": f"Here is My Homework for assignment {self.assignment}. Answer: {answer}. Please Grade it from 1 to 100 and provide short but valuable feedback while telling when and where marks are deducted in a section called Feedback.",
                }
            ],
            model=self.model_name,
            temperature=1.,
            max_tokens=1000,
            top_p=1.
        )
        return response.choices[0].message.content

    def extract_marks_and_feedback(self, grading_response):
        # Regular expression to extract marks
        marks_pattern = r'(\d+)\s*/\s*100'
        marks = re.search(marks_pattern, grading_response)
        marks = marks.group(1) if marks else "Marks not found"
        
        # Regular expression to extract feedback
        feedback_pattern = r'Feedback:\s*(.*)'
        feedback = re.search(feedback_pattern, grading_response, re.DOTALL)
        feedback = feedback.group(1).strip() if feedback else "Feedback not found"
        
        return marks, feedback

    def send_feedback(self, to_email, subject, feedback_message, from_email, from_password):
        try:
            # Creating the email headers and message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attaching the feedback message as the email body
            msg.attach(MIMEText(feedback_message, 'plain'))
            
            # Setting up the SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)  
            server.starttls()  
            
            # Logging into the sender's email account
            server.login(from_email, from_password)
            
            # Sending the email
            server.send_message(msg)
            server.quit()
            print(f"Feedback sent successfully to {to_email}.")
            
        except Exception as e:
            print(f"Error sending email to {to_email}: {str(e)}")


# Example usage
if __name__ == '__main__':
    # Reading the API token
    with open('git_hub_key.txt') as file:
        token = file.readline().strip()

    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o-mini"
    assignment = 'You are given a list of numbers. Make a function for finding unique elements'
    
    grader = HomeworkGrader(token, endpoint, model_name, assignment)
    
    # Example student's answer
    answer = 'def unique(arr):\n return set(arr)'
    
    # Get the grading response
    grading_response = grader.grade_answer(answer)
    
    # Extract marks and feedback
    marks, feedback = grader.extract_marks_and_feedback(grading_response)
    
    # Print marks and feedback to the terminal
    print(f"Marks: {marks}")
    print(f"Feedback: {feedback}")
    
    # Create the feedback message
    feedback_message = f"""
    Hello,

    Here is your feedback for the assessment:

    Score: {marks}/100
    {feedback}

    Best regards,
    Autograding System
    """

    # Email details
    student_email = "glennamayola05@gmail.com"  # Replace with actual student email
    from_email = "21a12.glenna@sjec.ac.in"  # Replace with your email
    from_password = "tdge xdrz rrso yvgr"  # Replace with your email password

    # Send the feedback via email
    grader.send_feedback(student_email, "Assessment Feedback", feedback_message, from_email, from_password)
