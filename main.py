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


def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /nonsk4 to check cards.')


def handle_nonsk4_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    username = update.message.from_user.username
    file = context.bot.get_file(update.message.document.file_id)

    total_accounts = []
    file.download('cc_list.txt')

    with open('cc_list.txt', 'r') as f:
        total_accounts = f.readlines()

    start_time = time.time()
    approved = []
    declined = []

    initial_message = "Checking Your Card.\n\n"
    keyboard = [
        [InlineKeyboardButton("CC", callback_data='cc')],
        [InlineKeyboardButton("Approved ✅", callback_data='approved')],
        [InlineKeyboardButton("Declined ❌", callback_data='declined')],
        [InlineKeyboardButton("Total Cards", callback_data='total')],
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


def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("text/plain"), handle_nonsk4_command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main() 
