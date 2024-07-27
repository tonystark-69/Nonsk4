
import requests
import json
import time
import os
import uuid
from websocket import create_connection
from ssl import CERT_NONE
from gzip import decompress
from random import choice, choices
from concurrent.futures import ThreadPoolExecutor

failed = 0
success = 0
retry = 0
accounts = []

def work():
    global failed, success, retry, accounts
    username = choice('qwertyuioplkjhgfdsazxcvbnm') + ''.join(choices(list('qwertyuioplkjhgfdsazxcvbnm1234567890'), k=12))
    try:
        con = create_connection(
            "wss://193.200.173.45/Auth",
            header={
                "app": "com.safeum.android",
                "host": None,
                "remoteIp": "193.200.173.45",
                "remotePort": str(8080),
                "sessionId": "b6cbb22d-06ca-41ff-8fda-c0ddeb148195",
                "time": "2023-04-30 12:13:32",
                "url": "wss://51.79.208.190/Auth"
            },
            sslopt={"cert_reqs": CERT_NONE}
        )
        con.send(json.dumps({
            "action": "Register",
            "subaction": "Desktop",
            "locale": "en_GB",
            "gmt": "+02",
            "password": {
                "m1x": "503c73d12b354f86ff9706b2114704380876f59f1444133e62ca27b5ee8127cc",
                "m1y": "6387ae32b7087257452ae27fc8a925ddd6ba31d955639838249c02b3de175dfc",
                "m2": "219d1d9b049550f26a6c7b7914a44da1b5c931eff8692dbfe3127eeb1a922fcf",
                "iv": "e38cb9e83aef6ceb60a7a71493317903",
                "message": "0d99759f972c527722a18a74b3e0b3c6060fe1be3ad53581a7692ff67b7bb651a18cde40552972d6d0b1482e119abde6203f5ab4985940da19bb998bb73f523806ed67cc6c9dbd310fd59fedee420f32"
            },
            "magicword": {
                "m1x": "04eb364e4ef79f31f3e95df2a956e9c72ddc7b8ed4bf965f4cea42739dbe8a4a",
                "m1y": "ef1608faa151cb7989b0ba7f57b39822d7b282511a77c4d7a33afe8165bdc1ab",
                "m2": "4b4d1468bfaf01a82c574ea71c44052d3ecb7c2866a2ced102d0a1a55901c94b",
                "iv": "b31d0165dde6b3d204263d6ea4b96789",
                "message": "8c6ec7ce0b9108d882bb076be6e49fe2"
            },
            "magicwordhint": "0000",
            "login": str(username),
            "devicename": "Xiaomi Redmi Note 8 Pro",
            "softwareversion": "1.1.0.1380",
            "nickname": "hvtctchnjvfxfx",
            "os": "AND",
            "deviceuid": "c72d110c1ae40d50",
            "devicepushuid": "*dxT6B6Solm0:APA91bHqL8wxzlyKHckKxMDz66HmUqmxCPAVKBDrs8KcxCAjwdpxIPTCfRmeEw8Jks_q13vOSFsOVjCVhb-CkkKmTUsaiS7YOYHQS_pbH1g6P4N-jlnRzySQwGvqMP1gxRVksHiOXKKP",
            "osversion": "and_11.0.0",
            "id": "1734805700"
        }))
        gzip = decompress(con.recv()).decode('utf-8')
        if '"status":"Success"' in gzip:
            success += 1
            accounts.append(username + ':hhhh')
            with open('SafeUM-Accounts.txt', 'a') as f:
                f.write(username + ":hhhh | \n")
        else:
            failed += 1
    except:
        retry += 1

def create_accounts(num_accounts):
    global failed, success, retry, accounts
    start_time = time.time()
    failed = 0
    success = 0
    retry = 0
    accounts = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(work) for _ in range(num_accounts)]
        for future in futures:
            future.result()

    elapsed_time = time.time() - start_time
    return success, retry, failed, elapsed_time, accounts

def get_footer_info(total_accounts, elapsed_time, username):
    footer = (
        f"－－－－－－－－－－－－－－－－\\n"
        f"🔹 Total Accounts Created - {total_accounts}\\n"
        f"⏱️ Time Taken - {elapsed_time:.2f} seconds\\n"
        f"▫️ Checked by: {username}\\n"
        f"⚡️ Bot by - AFTAB 👑\\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer
