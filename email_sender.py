import pandas as pd
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        """
        Initialize the EmailSender with SMTP configuration and logging.

        :param smtp_server: SMTP server address
        :param smtp_port: SMTP server port
        :param sender_email: Sender's email address
        :param sender_password: Sender's email password
        """

        logging.basicConfig(
            filename='email_sender.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # SMTP configuration
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def check_user_exists(self, email, df):
        """
        Check if a user exists for the given email.

        :param email: Email to check
        :param df: DataFrame containing user information
        :return: True if user exists, False otherwise
        """

        user_exists = not df[(df['MAIL'] == email) & (df['Predicted_Value'] == 1)].empty
        return user_exists

    def send_email(self, recipient_email, subject, body, df):
        """
        Send an email with comprehensive error handling and logging.

        :param recipient_email: Recipient's email address
        :param subject: Email subject
        :param body: Email body
        :param df: DataFrame to check user existence
        :return: Boolean indicating email sending success
        """

        if not self.check_user_exists(recipient_email, df):
            self.logger.warning(f"No user found for email: {recipient_email}")
            return False

        try:

            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))


            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)


                server.sendmail(self.sender_email, recipient_email, msg.as_string())


                self.logger.info(f"Email sent successfully to {recipient_email}")
                return True

        except smtplib.SMTPAuthenticationError:
            self.logger.error("SMTP Authentication Failed. Check credentials.")
            return False
        except smtplib.SMTPException as smtp_error:
            self.logger.error(f"SMTP Error sending to {recipient_email}: {smtp_error}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error sending to {recipient_email}: {e}")
            return False


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "brucewayne10gotham@gmail.com"
SENDER_PASSWORD = "ltcv odlx cord gope"

def send_emails():
    """
    Main function to send emails to selected candidates.
    Reads from output.csv and sends emails to candidates with Predicted_Value of 1.
    """


    email_sender = EmailSender(SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD)


    subject = "Interview Invitation for Python Developer Role at Wayne Enterprises"
    body = """Dear Candidate, 

We are pleased to inform you that after careful consideration of your application, you have been shortlisted for the position of Python Developer at Wayne Enterprises. Congratulations!

We were impressed with your background, skills, and experience, and we would like to invite you to the next stage of our selection process — "an interview with our team".
Our HR team will be reaching out shortly to coordinate the interview schedule and provide further details.
In the meantime, if you have any questions, please don’t hesitate to reach out. We look forward to speaking with you and exploring the potential of having you on our team.

Best Regards,
Hiring Team
Wayne Enterprises"""

    try:

        df = pd.read_csv("output.csv", delimiter=',')


        successful_emails = []
        no_user_emails = []
        failed_emails = []


        email_list = df["MAIL"].dropna().unique()

        # Send emails
        for email in email_list:
            try:
                if email_sender.send_email(email, subject, body, df):
                    successful_emails.append(email)
                else:
                    no_user_emails.append(email)
            except Exception as e:
                failed_emails.append(email)
                print(f"Error processing {email}: {e}")


        # Write failed emails to a file
        if failed_emails:
            with open('failed_emails.txt', 'w') as f:
                f.write("Failed Email Addresses:\n")
                for email in failed_emails:
                    f.write(f"{email}\n")

        print(f"Email sending completed.")
        print(f"Successful emails: {len(successful_emails)}")
        print(f"Failed emails: {len(failed_emails)}")


        logging.info(f"Email batch completed.")
        logging.info(f"Successful emails: {len(successful_emails)}")
        logging.info(f"Failed emails: {len(failed_emails)}")


        if no_user_emails:
            print("\nEmails with No Associated User:")
            for email in no_user_emails:
                print(email)

    except FileNotFoundError:
        print("Error: output.csv file not found.")
        logging.error("output.csv file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    send_emails()