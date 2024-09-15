import smtplib, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_feedback(to_email, subject, feedback_message, from_email, from_password):
    try:
        # Creating the email headers and message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attaching the feedback message as the email body
        msg.attach(MIMEText(feedback_message, 'plain'))
        
        # Setting up the SMTP server
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)  
        server.starttls()  
        
        
        server.login(from_email, from_password)   #login to senders email account
        
        
        server.send_message(msg)     #send the mail
        server.quit()
        print(f"Feedback sent successfully to {to_email}.")
        
    except Exception as e:
        print(f"Error sending email to {to_email}: {str(e)}")

def extract_marks_and_feedback(grading_response):
        # Regular expression to extract marks
        marks_pattern = r'(\d+)\s*/\s*100'
        marks = re.search(marks_pattern, grading_response)
        marks = marks.group(1) if marks else "Marks not found"
        
        # Regular expression to extract feedback
        feedback_pattern = r'Feedback:\s*(.*)'
        feedback = re.search(feedback_pattern, grading_response, re.DOTALL)
        feedback = feedback.group(1).strip() if feedback else "Feedback not found"
        
        return marks, feedback

if __name__ == "__main__":
    student_email = "example@gmail.com"  # Replace with actual student email
    feedback = """Hello, 

Here is your feedback for the assessment:

Score: 85/100
Comments: Great job! You can improve by optimizing your code further.

Best regards,
Autograding System
"""
    from_email = "example@gmail.com"  # Replace with your email
    from_password = "xxxxx"      # Replace with your email password 
    send_feedback(student_email, "Assessment Feedback", feedback, from_email, from_password)