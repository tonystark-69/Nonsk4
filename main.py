import telebot
import time
from keep_alive import keep_alive
import threading
from telebot import types
from nonsk4 import check_nonsk4, get_footer_info as nonsk4_footer_info
from gpt import check_gpt, get_footer_info as gpt_footer_info
#import crunchy
from crunchy import check_crunchy, get_footer_info
import os
import sys
import hotmail
import seedr
#from smsbd import check_smsbd, get_footer_info
#from safeum import create_accounts, get_footer_info

TOKEN = '7422696256:AAHV6Df2UShvfvrlFMTkSX8cki6KAMl0T7w'
bot = telebot.TeleBot(TOKEN)

# Dictionary to hold chat_id specific data
chat_data = {}
#stop_processing = False

def send_start_message(message):
    first_name = message.from_user.first_name
    welcome_message = (
        f"Hello there, {first_name}!\n"
        "I am Starboy, a simple account-checking bot. I'm still under development, "
        "so you might encounter some bugs.\n"
        "To see all commands, use /help.\n\n"
        "If you face any issues, feel free to contact @aftab_kabirr.\n\n"
        "Bot by: Aftab👑"
    )
    bot.reply_to(message, welcome_message)

@bot.message_handler(commands=['start'])
def start(message):
    send_start_message(message)
    
def send_help_message(message):
    help_message = (
        "Here are the available commands:\n\n"
        "/crunchy - Upload your combo and reply with the command.\n"
        "/hotmail - Upload your combo and reply with the command.\n"
        "/seedr - Upload your combo and reply with the command.\n"
        "/gpt - Upload your combo and reply with the command.\n"
        "/nonsk4 - Upload your combo and reply with the command.\n\n"
        "More commands coming soon...\n\n"
        "For any issues or inquiries, contact: @aftab_kabirr\n\n"
        "Bot by: Aftab👑"
    )
    bot.reply_to(message, help_message)

@bot.message_handler(commands=['help'])
def help_command(message):
    send_help_message(message)

@bot.message_handler(commands=['nonsk4'])
def nonsk4_command(message):
    if message.reply_to_message and message.reply_to_message.document:
        if message.reply_to_message.document.mime_type == 'text/plain':
            file_info = bot.get_file(message.reply_to_message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_content = downloaded_file.decode('utf-8')

            chat_id = message.chat.id
            username = message.from_user.username

            # Start a new thread to handle the file processing
            threading.Thread(target=process_nonsk4, args=(chat_id, username, file_content)).start()
        else:
            bot.reply_to(message, "Please reply to a valid txt file.")
    else:
        bot.reply_to(message, "Please reply to a txt file with the /nonsk4 command.")

@bot.message_handler(commands=['gpt'])
def gpt_command(message):
    if message.reply_to_message and message.reply_to_message.document:
        if message.reply_to_message.document.mime_type == 'text/plain':
            file_info = bot.get_file(message.reply_to_message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_content = downloaded_file.decode('utf-8')

            chat_id = message.chat.id
            username = message.from_user.username

            # Start a new thread to handle the file processing
            threading.Thread(target=process_gpt, args=(chat_id, username, file_content)).start()
        else:
            bot.reply_to(message, "Please reply to a valid txt file.")
    else:
        bot.reply_to(message, "Please reply to a txt file with the /gpt command.")

def process_nonsk4(chat_id, username, file_content):
    total_accounts = file_content.splitlines()
    start_time = time.time()
    approved = []
    declined = []

    initial_message = "Checking Your Card.\n\n"
    footer_info = nonsk4_footer_info(len(total_accounts), start_time, username)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("CC", callback_data=f"{chat_id}:cc"))
    markup.add(types.InlineKeyboardButton(f"Approved ✅: {len(approved)}", callback_data=f"{chat_id}:approved"))
    markup.add(types.InlineKeyboardButton(f"Declined ❌: {len(declined)}", callback_data=f"{chat_id}:declined"))
    markup.add(types.InlineKeyboardButton("Total Cards", callback_data=f"{chat_id}:total"))
    markup.add(types.InlineKeyboardButton("Stop", callback_data=f"{chat_id}:stop"))
    
    msg = bot.send_message(chat_id, initial_message + footer_info, reply_markup=markup)

    for account in total_accounts:
        result = check_nonsk4(account)
        if result == 'Approved':
            approved.append(account)
        else:
            declined.append(account)

        chat_data[chat_id] = {
            'approved': approved,
            'declined': declined,
            'total_accounts': total_accounts
        }

        live_update = f"Checking Your Card\nCC: {account}\nResult: {result}\n\n" + footer_info
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("CC", callback_data=f"{chat_id}:{account}"))
        markup.add(types.InlineKeyboardButton(f"Approved ✅: {len(approved)}", callback_data=f"{chat_id}:approved"))
        markup.add(types.InlineKeyboardButton(f"Declined ❌: {len(declined)}", callback_data=f"{chat_id}:declined"))
        markup.add(types.InlineKeyboardButton("Total Cards", callback_data=f"{chat_id}:total"))
        markup.add(types.InlineKeyboardButton("Stop", callback_data=f"{chat_id}:stop"))
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.message_id,
            text=live_update,
            reply_markup=markup
        )

    final_message = "↯ CHAT GPT\n\nGAME OVER⚡️\n\n－－－－－－－－－－－－－－－－\nOwner: Aftab👑\n－－－－－－－－－－－－－－－－"
    bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=final_message, reply_markup=markup)

def process_gpt(chat_id, username, file_content):
    total_accounts = file_content.splitlines()
    start_time = time.time()
    hits = []
    dead = []

    initial_message = "Checking Your Account.\n\n"
    footer_info = gpt_footer_info(len(total_accounts), start_time, username)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("CC", callback_data=f"{chat_id}:cc"))
    markup.add(types.InlineKeyboardButton(f"Hit ✅: {len(hits)}", callback_data=f"{chat_id}:hit"))
    markup.add(types.InlineKeyboardButton(f"Dead ❌: {len(dead)}", callback_data=f"{chat_id}:dead"))
    markup.add(types.InlineKeyboardButton("Total Accounts", callback_data=f"{chat_id}:total"))
    markup.add(types.InlineKeyboardButton("Stop", callback_data=f"{chat_id}:stop"))
    
    msg = bot.send_message(chat_id, initial_message + footer_info, reply_markup=markup)

    for account in total_accounts:
        user, password = account.split(":", 1)
        result, response_message = check_gpt(user, password)
        if result == 'Hit':
            hits.append(account)
        else:
            dead.append(account)

        chat_data[chat_id] = {
            'hits': hits,
            'dead': dead,
            'total_accounts': total_accounts
        }

        if result == 'Hit':
            live_update = f"↯ CHAT GPT\nCOMBO: {account}\nResult: HIT✅\nResponse:\n{response_message}\n\n" + footer_info
        else:
            live_update = f"↯ CHAT GPT\nCOMBO: {account}\nResult: Dead\nResponse: {response_message}\n\n" + footer_info

        # Update inline buttons with live count
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("CC", callback_data=f"{chat_id}:{account}"))
        markup.add(types.InlineKeyboardButton(f"Hit ✅: {len(hits)}", callback_data=f"{chat_id}:hit"))
        markup.add(types.InlineKeyboardButton(f"Dead ❌: {len(dead)}", callback_data=f"{chat_id}:dead"))
        markup.add(types.InlineKeyboardButton("Total Accounts", callback_data=f"{chat_id}:total"))
        markup.add(types.InlineKeyboardButton("Stop", callback_data=f"{chat_id}:stop"))
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.message_id,
            text=live_update,
            reply_markup=markup
        )

    final_message = "↯ CHAT GPT\n\nGAME OVER⚡️\n\n－－－－－－－－－－－－－－－－\nOwner: Aftab👑\n－－－－－－－－－－－－－－－－"
    bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=final_message, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    data = call.data.split(':')
    cmd = data[1]

    # Ensure chat_data contains the necessary keys
    if chat_id not in chat_data:
        bot.answer_callback_query(call.id, "No data available for this chat.")
        return

    if cmd == 'hit':
        hits_list = '\n'.join(chat_data[chat_id].get('hits', [])) if chat_data[chat_id].get('hits') else 'No hits yet.'
        bot.send_message(chat_id, f"Hit Accounts:\n{hits_list}")
    elif cmd == 'dead':
        dead_list = '\n'.join(chat_data[chat_id].get('dead', [])) if chat_data[chat_id].get('dead') else 'No dead accounts yet.'
        bot.send_message(chat_id, f"Dead Accounts:\n{dead_list}")
    elif cmd == 'total':
        pass  # Do nothing
   

@bot.message_handler(commands=['crunchy'])
def crunchy_command(message):
    if message.reply_to_message and message.reply_to_message.document:
        if message.reply_to_message.document.mime_type == 'text/plain':
            file_info = bot.get_file(message.reply_to_message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_content = downloaded_file.decode('utf-8')

            chat_id = message.chat.id
            username = message.from_user.username

            # Start a new thread to handle the file processing
            threading.Thread(target=process_crunchy, args=(chat_id, username, file_content)).start()
        else:
            bot.reply_to(message, "Please reply to a valid txt file.")
    else:
        bot.reply_to(message, "Please reply to a txt file with the /crunchy command.")

def process_crunchy(chat_id, username, file_content):
    total_accounts = file_content.splitlines()
    start_time = time.time()

    hits = []
    dead = []

    initial_message = "Checking Your Accounts...\n\n"
    footer_info = get_footer_info(len(total_accounts), start_time, username)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"Hit ✅: 0", callback_data=f"{chat_id}:hit"))
    markup.add(types.InlineKeyboardButton(f"Dead ❌: 0", callback_data=f"{chat_id}:dead"))

    msg = bot.send_message(chat_id, initial_message + footer_info, reply_markup=markup, parse_mode='HTML')

    for account in total_accounts:
        email, password = account.split(":", 1)
        result, response_message = check_crunchy(email, password)

        if result == 'Hit':
            hits.append(f"<code>{account}</code>")
        else:
            dead.append(f"<code>{account}</code>")

        chat_data[chat_id] = {
            'hits': hits,
            'dead': dead,
            'total_accounts': len(total_accounts)
        }

        live_update = (
            f"↯ CRUNCHY CHECKER\n\n"
            f"➣Combo: {account}\n"
            f"➣Result: {result}\n"
            f"➣Response: {response_message}\n"
            f"{get_footer_info(len(total_accounts), start_time, username)}"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"Hit ✅: {len(hits)}", callback_data=f"{chat_id}:hit"))
        markup.add(types.InlineKeyboardButton(f"Dead ❌: {len(dead)}", callback_data=f"{chat_id}:dead"))

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.message_id,
            text=live_update,
            reply_markup=markup,
            parse_mode='HTML'
        )

    final_message = (
        f"↯ CRUNCHY CHECKER\n⇒ GAME OVER\n\n"
        f"⤬ Summary\n"
        f"Total : {len(total_accounts)}\n"
        f"LIVE : {len(hits)}\n"
        f"DEAD: {len(dead)}\n\n"
        f"{footer_info}"
    )
    bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=final_message, parse_mode='HTML')

    if hits:
        hit_accounts = '\n'.join(hits)
        bot.send_message(chat_id, f"↯ HITS\n\n{hit_accounts}", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    data = call.data.split(':')
    cmd = data[1]

    if chat_id not in chat_data:
        bot.answer_callback_query(call.id, "No data available for this chat.")
        return

    if cmd == 'hit':
        hits_list = '\n'.join(chat_data[chat_id].get('hits', [])) if chat_data[chat_id].get('hits') else 'No hits yet.'
        bot.send_message(chat_id, f"↯ HITS\n\n{hits_list}", parse_mode='HTML')

    elif cmd == 'dead':
        dead_list = '\n'.join(chat_data[chat_id].get('dead', [])) if chat_data[chat_id].get('dead') else 'No dead accounts yet.'
        bot.send_message(chat_id, f"↯ DEAD\n\n{dead_list}", parse_mode='HTML')
        
@bot.message_handler(commands=['hotmail'])
def hotmail_command(message):
    if message.reply_to_message and message.reply_to_message.document:
        if message.reply_to_message.document.mime_type == 'text/plain':
            file_info = bot.get_file(message.reply_to_message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_content = downloaded_file.decode('utf-8')

            chat_id = message.chat.id
            username = message.from_user.username

            threading.Thread(target=process_hotmail, args=(chat_id, username, file_content)).start()
        else:
            bot.reply_to(message, "Please reply to a valid txt file.")
    else:
        bot.reply_to(message, "Please reply to a txt file with the /hotmail command.")

def process_hotmail(chat_id, username, file_content):
    total_accounts = file_content.splitlines()
    start_time = time.time()
    hits = []
    dead = []

    initial_message = "Checking Your Account.\n\n"
    footer_info = hotmail.get_footer_info(len(total_accounts), start_time, username)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"Hit ✅: {len(hits)}", callback_data=f"{chat_id}:hit"))
    markup.add(types.InlineKeyboardButton(f"Dead ❌: {len(dead)}", callback_data=f"{chat_id}:dead"))

    msg = bot.send_message(chat_id, initial_message + footer_info, reply_markup=markup)

    for account in total_accounts:
        email, password = account.split(":", 1)
        result, response_message = hotmail.check_hotmail(email, password)
        if result == 'Hit':
            hits.append(account)
        else:
            dead.append(account)

        chat_data[chat_id] = {
            'hits': hits,
            'dead': dead,
            'total_accounts': total_accounts
        }

        live_update = f"↯ HOTMAIL CHECKER\n\n➣COMBO: {account}\n➣Result: {result}\n✦Response: {response_message}\n\n" + footer_info

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"Hit ✅: {len(hits)}", callback_data=f"{chat_id}:hit"))
        markup.add(types.InlineKeyboardButton(f"Dead ❌: {len(dead)}", callback_data=f"{chat_id}:dead"))

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.message_id,
            text=live_update,
            reply_markup=markup
        )

    final_message = (
        f"↯ HOTMAIL CHECKER\n⇒ GAME OVER\n\n"
        f"⤬ Summary\n"
        f"Total : {len(total_accounts)}\n"
        f"LIVE : {len(hits)}\n"
        f"DEAD: {len(dead)}\n\n"
        f"{footer_info}"
    )
    bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=final_message)

    if hits:
        hit_accounts = '\n'.join(hits)
        bot.send_message(chat_id, f"↯HITS\n\n{hit_accounts}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    data = call.data.split(':')
    cmd = data[1]

    if chat_id not in chat_data:
        bot.answer_callback_query(call.id, "No data available for this chat.")
        return

    if cmd == 'hit':
        hits_list = '\n'.join(chat_data[chat_id].get('hits', [])) if chat_data[chat_id].get('hits') else 'No hits yet.'
        bot.send_message(chat_id, f"↯HITS\n{hits_list}")
    elif cmd == 'dead':
        dead_list = '\n'.join(chat_data[chat_id].get('dead', [])) if chat_data[chat_id].get('dead') else 'No dead accounts yet.'
        bot.send_message(chat_id, f"Dead Accounts:\n{dead_list}")

@bot.message_handler(commands=['seedr'])
def seedr_command(message):
    if message.reply_to_message and message.reply_to_message.document:
        if message.reply_to_message.document.mime_type == 'text/plain':
            file_info = bot.get_file(message.reply_to_message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_content = downloaded_file.decode('utf-8')

            chat_id = message.chat.id
            username = message.from_user.username

            threading.Thread(target=process_seedr, args=(chat_id, username, file_content)).start()
        else:
            bot.reply_to(message, "Please reply to a valid txt file.")
    else:
        bot.reply_to(message, "Please reply to a txt file with the /seedr command.")

def process_seedr(chat_id, username, file_content):
    total_accounts = file_content.splitlines()
    start_time = time.time()
    hits = []
    dead = []

    initial_message = "Checking Your Accounts...\n\n"
    footer_info = seedr.get_footer_info(len(total_accounts), start_time, username)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"Hit ✅: {len(hits)}", callback_data=f"{chat_id}:hit"))
    markup.add(types.InlineKeyboardButton(f"Dead ❌: {len(dead)}", callback_data=f"{chat_id}:dead"))

    msg = bot.send_message(chat_id, initial_message + footer_info, reply_markup=markup)

    for account in total_accounts:
        email, password = account.split(":", 1)
        result, response_message = seedr.check_seedr_account(email, password)
        if result == 'Hit':
            hits.append(account)
        else:
            dead.append(account)

        chat_data[chat_id] = {
            'hits': hits,
            'dead': dead,
            'total_accounts': total_accounts
        }

        live_update = f"↯ SEEDR CHECKER\n\n➣COMBO: {account}\n➣Result: {result}\n✦Response: {response_message}\n\n" + footer_info

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"Hit ✅: {len(hits)}", callback_data=f"{chat_id}:hit"))
        markup.add(types.InlineKeyboardButton(f"Dead ❌: {len(dead)}", callback_data=f"{chat_id}:dead"))

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.message_id,
            text=live_update,
            reply_markup=markup
        )

    final_message = (
        f"↯ SEEDR CHECKER\n⇒ GAME OVER\n\n"
        f"⤬ Summary\n"
        f"Total : {len(total_accounts)}\n"
        f"LIVE : {len(hits)}\n"
        f"DEAD: {len(dead)}\n\n"
        f"{footer_info}"
    )
    bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=final_message)

    if hits:
        hit_accounts = '\n'.join(hits)
        bot.send_message(chat_id, f"↯HITS\n\n{hit_accounts}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    data = call.data.split(':')
    cmd = data[1]

    if chat_id not in chat_data:
        bot.answer_callback_query(call.id, "No data available for this chat.")
        return

    if cmd == 'hit':
        hits_list = '\n'.join(chat_data[chat_id].get('hits', [])) if chat_data[chat_id].get('hits') else 'No hits yet.'
        bot.send_message(chat_id, f"↯HITS\n{hits_list}")
    elif cmd == 'dead':
        dead_list = '\n'.join(chat_data[chat_id].get('dead', [])) if chat_data[chat_id].get('dead') else 'No dead accounts yet.'
        bot.send_message(chat_id, f"Dead Accounts:\n{dead_list}")
'''
@bot.message_handler(commands=['safeum'])
def handle_safeum(message):
    msg = bot.reply_to(message, "How many accounts do you need?")
    bot.register_next_step_handler(msg, process_account_count)

def process_account_count(message):
    try:
        num_accounts = int(message.text)
        username = message.from_user.username
        start_time = time.time()

        success, retry, failed, elapsed_time, accounts = create_accounts(num_accounts)

        result_message = (
            f"↯ SAFEUM ACCOUNT CREATION RESULTS ↯\n"
            f"🔹 Success: {success}\n"
            f"🔹 Retry: {retry}\n"
            f"🔹 Failed: {failed}\n"
            f"⏱️ Time Taken: {elapsed_time:.2f} seconds\n"
        )
        bot.send_message(message.chat.id, result_message)

        footer = get_footer_info(success, elapsed_time, username)
        bot.send_message(message.chat.id, footer)

        accounts_message = '\n'.join(accounts)
        bot.send_message(message.chat.id, f"Accounts:\n{accounts_message}")
    except ValueError:
        bot.reply_to(message, "Please enter a valid number.")
'''
if __name__ == "__main__":
    keep_alive()
    bot.polling()
