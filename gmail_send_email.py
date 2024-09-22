from dotenv import load_dotenv
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Gemini_API_Reponse import create_email_prompt, extract_resume_sections, gemini_reponse, create_cover_letter
from input import job_title,job_description,Company_Name
from email.mime.base import MIMEBase
from email import encoders


env_path = 'Config.env'
load_dotenv(dotenv_path=env_path)

EMAIL = os.getenv('GMAIL_EMAIL')
PASSWORD = os.getenv('GMAIL_PASSWORD')
Resume_path= "C:/Users/hrith.DESKTOP-75K32P0/OneDrive/Documents/Hrithik_Files_Desktop/FT_Resumes_NEU/Hrithik_Resume_Data_Engineer_UPD.pdf"

def send_email(to_email, subject, body, attachment_path=None):
    # Set your name in the 'From' field
    from_name = "Hrithik Sarda"
    from_email = EMAIL
    full_from = f"{from_name} <{from_email}>"
    
    # Create the email headers
    msg = MIMEMultipart()
    msg['From'] = full_from
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach a PDF file if provided
    if attachment_path:
        attachment_name = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as attachment_file:
            attachment = MIMEBase('application', 'pdf')  # Specify 'pdf' content type
            attachment.set_payload(attachment_file.read())
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename={attachment_name}'
        )
        msg.attach(attachment)
    
    # Connect to Gmail's SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS encryption
        server.login(EMAIL, PASSWORD)  # Login to your Gmail account
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        print(f"Email successfully sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")
    finally:
        server.quit()  # Close the connection

def split_response(response):
    # Find the position where the body starts
    start_pos = response.find('Dear ')
    if start_pos != -1:
        subject = response[:start_pos].replace('#','').replace('Subject:','').strip()
        body = response[start_pos:].strip()
    else:
        subject = "No Subject"
        body = response.strip()
    return subject, body


def read_email_response(file_path):
    with open(file_path, 'r') as file:
        email_reponse = file.read()
    return email_reponse


def read_email_response(file_path):
    with open(file_path, 'r') as file:
        email_reponse = file.read()
    return email_reponse


def Email_Finalization(draft_email,validation_instructions):


    # Construct the prompt for the Gemini API
    prompt1 = f"""
    You are an email validation assistant. 
    Here are the instructions for validating and finalizing a job application email:
    {validation_instructions}


    Below is the draft email that needs to be validated and finalized based on the above instructions. 

    Draft Email:

    {draft_email}
    

    Please provide the final, ready-to-send version of the email.
    """


    # Extract the updated email from the response
    updated_email = gemini_reponse(prompt1)

    prompt2=  f"""
    You are an email Finalizing assistant.

    The change to the validated: 
    If any of the placeholders are missing and cannot be replaced with specific information, 
    simply remove them and adjust the email accordingly. The final output should be ready to send without any additional updates required.

    Below is the draft email that needs to be validated and finalized based on the above instructions. 

    Draft Email:
    {updated_email} 

    
    **Note:**
    If any of the placeholders are missing and cannot be replaced with specific information, 
    simply remove them and adjust the email accordingly. The final output should be ready to send without any additional updates required.



    

    Please provide the final, ready-to-send version of the email.
    """

    updated_email = gemini_reponse(prompt2)

    prompt3=  f"""
    You are an email Finalizing assistant.

    The change to be made: 
    If there is any email content within square brackets "[]", REMOVE IT and adjust the email accordingly. The final output should be ready to send without any additional updates required.

    Below is the draft email that needs to be validated and finalized based on the above instructions. 

    Draft Email:
    {updated_email} 

    
    **Note:**
    The change to be validated made: 
    If there is any content within square brackets "[]", REMOVE IT and adjust the email accordingly. The final output should be ready to send without any additional updates required.




    

    Please provide the final, ready-to-send version of the email.
    """

    updated_email = gemini_reponse(prompt3)


    return updated_email


def CV_Finalization(draft_CV,validation_instructions):


    # Construct the prompt for the Gemini API
    prompt1 = f"""
    You are an Cover Letter Writer assistant. 
    Here are the instructions for validating and finalizing a job application Cover Letter:
    {validation_instructions}


    Below is the draft Cover Letter that needs to be validated and finalized based on the above instructions. 

    Draft Cover Letter:

    {draft_CV}
    

    Please provide the final, ready-to-send version of the Cover Letter.
    """


    # Extract the updated email from the response
    updated_CV = gemini_reponse(prompt1)

    prompt2=  f"""
    You are a Cover Letter Finalizing assistant.

    The change to the validated: 
    If any of the placeholders are missing and cannot be replaced with specific information, 
    simply remove them and adjust the Cover Letter accordingly. The final output should be ready to send without any additional updates required.

    Below is the draft Cover Letter that needs to be validated and finalized based on the above instructions. 

    Draft Cover Letter:
    {updated_CV} 

    
    **Note:**
    If any of the placeholders are missing and cannot be replaced with specific information, 
    simply remove them and adjust the Cover Letter accordingly. The final output should be ready to send without any additional updates required.



    

    Please provide the final, ready-to-send version of the Cover Letter.
    """

    updated_CV = gemini_reponse(prompt2)

    prompt3=  f"""
    You are an Cover Letter Finalizing assistant.

    The change to be made: 
    If there is any Cover Letter content within square brackets "[]", REMOVE IT and adjust the Cover Letter accordingly. The final output should be ready to send without any additional updates required.

    Below is the draft Cover Letter that needs to be validated and finalized based on the above instructions. 

    Draft Cover Letter:
    {updated_CV} 

    
    **Note:**
    Include my contact details as follows :
    My name is Hrithik Sarda. My email address is hrithiksarda4@gmail.com, and my phone number is +1 (978)-654-0445.
    The change to be validated made: 
    If there is any content within square brackets "[]", REMOVE IT and adjust the Cover Letter accordingly. The final output should be ready to send without any additional updates required.




    

    Please provide the final, ready-to-send version of the Cover Letter.
    """

    updated_CV = gemini_reponse(prompt3)


    return updated_CV




def main():
    # Extract resume sections and create email prompt
    resume_sections = extract_resume_sections(Resume_path)

    choice = input("Please choose an option: \n1 for Email Generation and Sending\n2 for Just Generating a Cover Letter\nEnter your choice (1 or 2): ")

    if choice == '1':
        print("You chose Email Generation and Sending.")
        # Add logic for email generation and sending


        prompt = create_email_prompt(resume_sections, job_title, Company_Name, job_description)
        response = gemini_reponse(prompt)
        

        # Write response to file
        with open('Email_Response.txt', 'w') as file:
            file.write(response)
        
        with open("Email_Response.txt", "r") as file:
            draft_email = file.read()

        with open("LLM_Email_Validation_Instructions.txt", "r") as file:
            validation_instructions = file.read()


        updated_email= Email_Finalization(draft_email,validation_instructions)
        
        with open("Updated_Final_Email.txt", "w") as file:
            file.write(updated_email)

        print("The final send-ready email has been saved to Updated_Final_Email.txt")    
        
        # Read the response and split into subject and body
        email_response = read_email_response('Updated_Final_Email.txt')
        subject, body = split_response(email_response)
        
        # Define recipients and send email
        recipients = ["hrithiksarda1999@gmail.com"]
        for recipient in recipients:
            send_email(recipient, subject, body, attachment_path=Resume_path)
    
    elif choice == '2':
        print("You chose Just Generating a Cover Letter.")
        prompt = create_cover_letter(resume_sections, job_title, Company_Name, job_description)
        #print('1')
        response = gemini_reponse(prompt)
        #print('2')

        # Write response to file
        with open('Draft_Cover_Letter.txt', 'w') as file:
            file.write(response)
        
        with open("Draft_Cover_Letter.txt", "r") as file:
            draft_CV = file.read()

        with open("LLM_Cover_Letter_Instructions.txt", "r") as file:
            validation_instructions = file.read()


        updated_CV= Email_Finalization(draft_CV,validation_instructions)

        #print('3')
        
        with open("Final_Cover_Letter.txt", "w") as file:
            file.write(updated_CV)

        print("The final send-ready Cover Letter has been saved to Final_Cover_letter.txt")         
    else:
        print("Invalid choice. Please enter 1 or 2.")



if __name__ == "__main__":
    main()







