import smtplib
import traceback
import concurrent.futures

def check(subject, body, to_email, sender_email, sender_password):
    try:
        message = f"Subject: {subject}\n\n{body}"
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message)
        server.quit()

        return None
    except smtplib.SMTPAuthenticationError:
        return "Authentication failed."
    except Exception as e:
        error_message = f"{str(e)}\n{traceback.format_exc()}"
        return error_message

def check_emailpass(emailpass):
    e = str(emailpass).split(':')
    return emailpass, check('Checking...', 'Checking...', e[0], e[0], e[1])
