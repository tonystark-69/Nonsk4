import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from nonsk4 import check_nonsk4, get_footer_info
import time

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = '7422696256:AAHV6Df2UShvfvrlFMTkSX8cki6KAMl0T7w'
approved = []
declined = []
total_accounts = []

def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /nonsk4 to check cards.')

def nonsk4_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Please provide the combo as a txt file.')

def handle_document(update: Update, context: CallbackContext) -> None:
    if update.message.document.mime_type == 'text/plain':
        file_info = context.bot.get_file(update.message.document.file_id)
        downloaded_file = context.bot.download_file(file_info.file_path)

        with open('cc_list.txt', 'wb') as f:
            f.write(downloaded_file)

        with open('cc_list.txt', 'r') as f:
            global total_accounts
            total_accounts = f.readlines()

        chat_id = update.message.chat.id
        username = update.message.from_user.username
        start_time = time.time()
        global approved, declined
        approved = []
        declined = []

        initial_message = "Checking Your Card.\n\n"
        keyboard = [
            [InlineKeyboardButton("CC", callback_data='cc')],
            [InlineKeyboardButton(f"Approved ✅: {len(approved)}", callback_data='approved')],
            [InlineKeyboardButton(f"Declined ❌: {len(declined)}", callback_data='declined')],
            [InlineKeyboardButton(f"Total Cards: {len(total_accounts)}", callback_data='total')],
            [InlineKeyboardButton("Stop", callback_data='stop')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = context.bot.send_message(chat_id=chat_id, text=initial_message, reply_markup=reply_markup)

        for account in total_accounts:
            result = check_nonsk4(account)
            if result == 'Approved':
                approved.append(account)
            else:
                declined.append(account)
            keyboard = [
                [InlineKeyboardButton("CC", callback_data=account)],
                [InlineKeyboardButton(f"Approved ✅: {len(approved)}", callback_data='approved')],
                [InlineKeyboardButton(f"Declined ❌: {len(declined)}", callback_data='declined')],
                [InlineKeyboardButton(f"Total Cards: {len(total_accounts)}", callback_data='total')],
                [InlineKeyboardButton("Stop", callback_data='stop')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + get_footer_info(len(total_accounts), start_time, username),
                reply_markup=reply_markup
            )

        final_message = "Card is finished checking.\n\nDeveloper :@aftab"
        context.bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=final_message)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    global approved, declined, total_accounts

    if query.data == 'approved':
        approved_list = '\n'.join(approved) if approved else 'No approved cards yet.'
        context.bot.send_message(chat_id=query.message.chat.id, text=f"Approved Cards:\n{approved_list}")
    elif query.data == 'declined':
        declined_list = '\n'.join(declined) if declined else 'No declined cards yet.'
        context.bot.send_message(chat_id=query.message.chat.id, text=f"Declined Cards:\n{declined_list}")
    elif query.data == 'total':
        query.edit_message_text(text=f"Total Cards: {len(total_accounts)}")
    elif query.data == 'stop':
        query.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="Processing stopped by user.")

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("nonsk4", nonsk4_command))
    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("text/plain"), handle_document))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
