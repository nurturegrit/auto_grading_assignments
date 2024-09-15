import smtplib
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
        server = smtplib.SMTP('smtp.gmail.com', 587)  
        server.starttls()  
        
        
        server.login(from_email, from_password)   #login to senders email account
        
        
        server.send_message(msg)     #send the mail
        server.quit()
        print(f"Feedback sent successfully to {to_email}.")
        
    except Exception as e:
        print(f"Error sending email to {to_email}: {str(e)}")


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