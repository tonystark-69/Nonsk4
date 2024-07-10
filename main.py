import os
import sys
import time
import threading
import telebot
from telebot import types
from flask import Flask, request

from nonsk4 import check_nonsk4, get_footer_info

TOKEN = '7422696256:AAHV6Df2UShvfvrlFMTkSX8cki6KAMl0T7w'
bot = telebot.TeleBot(TOKEN)

# Flask setup for keep-alive
app = Flask(__name__)

# Dictionary to hold chat_id specific data
chat_data = {}
stop_processing = False

def send_start_message(message):
    bot.reply_to(message, "Hi! Use /nonsk4 in reply to a txt file to check cards. Use /restart to restart the bot and /stop to stop all checks.")

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
            threading.Thread(target=process_document, args=(chat_id, username, file_content)).start()
        else:
            bot.reply_to(message, "Please reply to a valid txt file.")
    else:
        bot.reply_to(message, "Please reply to a txt file with the /nonsk4 command.")

@bot.message_handler(commands=['restart'])
def restart_command(message):
    bot.reply_to(message, "Restarting the bot...")
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.message_handler(commands=['stop'])
def stop_command(message):
    global stop_processing
    stop_processing = True
    bot.reply_to(message, "Stopping all ongoing checks...")

def process_document(chat_id, username, file_content):
    global stop_processing
    total_accounts = file_content.splitlines()
    start_time = time.time()
    approved = []
    declined = []

    initial_message = "Checking Your Card.\n\n"
    footer_info = get_footer_info(len(total_accounts), start_time, username)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("CC", callback_data=f"{chat_id}:cc"))
    markup.add(types.InlineKeyboardButton(f"Approved ✅: {len(approved)}", callback_data=f"{chat_id}:approved"))
    markup.add(types.InlineKeyboardButton(f"Declined ❌: {len(declined)}", callback_data=f"{chat_id}:declined"))
    markup.add(types.InlineKeyboardButton("Total Cards", callback_data=f"{chat_id}:total"))
    markup.add(types.InlineKeyboardButton("Stop", callback_data=f"{chat_id}:stop"))
    
    msg = bot.send_message(chat_id, initial_message + footer_info, reply_markup=markup)

    for account in total_accounts:
        if stop_processing:
            bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text="Processing stopped by user.")
            return

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

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    data = call.data.split(':')
    cmd = data[1]

    # Ensure chat_data contains the necessary keys
    if chat_id not in chat_data:
        bot.answer_callback_query(call.id, "No data available for this chat.")
        return

    if cmd == 'approved':
        approved_list = '\n'.join(chat_data[chat_id].get('approved', [])) if chat_data[chat_id].get('approved') else 'No approved cards yet.'
        bot.send_message(chat_id, f"Approved Cards:\n{approved_list}")
    elif cmd == 'declined':
        declined_list = '\n'.join(chat_data[chat_id].get('declined', [])) if chat_data[chat_id].get('declined') else 'No declined cards yet.'
        bot.send_message(chat_id, f"Declined Cards:\n{declined_list}")
    elif cmd == 'total':
        pass  # Do nothing
    elif cmd == 'stop':
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Processing stopped by user.")

@app.route('/')
def index():
    return 'Bot is running'

if __name__ == '__main__':
    threading.Thread(target=lambda: bot.polling()).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
