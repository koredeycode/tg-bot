import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext

TOKEN = "5671094663:AAGgo4DPNZlN-LdoFt9m_mD47BQb4QSzFTw"
BOT_USERNAME = "tunny2706bot"
dash_keys = [['Twitter', 'Discord', 'ETH address'], [
    'Referral Link', 'Referred'], ['Balance', 'Details']]
dash_markup = ReplyKeyboardMarkup(dash_keys, resize_keyboard=True)
inline_markup = InlineKeyboardMarkup([[InlineKeyboardButton(
    "Help", callback_data="/help")]])


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    date = update.message.date
    reply = (f"""
        First Name: {user.first_name}
        Id: {user.id}
        Is_bot: {user.is_bot}
        UserName: {user.username}
        Date: {date}
        """)
    await update.message.reply_text(reply, reply_markup=inline_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Howw cn i help you")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("this is a custom command, you can add what you want")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # message_type: str = update.message.chat.type
    text: str = update.message.text
    response = f"you sent: {text}"
    await update.message.reply_text(response)


async def handle_callback(update: Update, context: CallbackContext):
    print(update.to_json())


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_error_handler(error)

    print("polling...")
    app.run_polling(poll_interval=3)
