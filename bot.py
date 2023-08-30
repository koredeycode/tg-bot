from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext

inline_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("Info", callback_data="Info")],
    [InlineKeyboardButton("Date", callback_data="Date")],
])


class MyBot:
    def __init__(self, token):
        bot = ApplicationBuilder().token(token).build()
        bot.add_handler(CommandHandler('start', self.handle_start))
        bot.add_handler(CommandHandler('help', self.handle_help))
        bot.add_handler(CallbackQueryHandler(self.handle_callback))
        self.bot = bot

    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(update)
        await update.message.reply_text("Welcome to Mybot", reply_markup=inline_markup)

    async def handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("how can i help you")

    async def handle_callback(self, update: Update, context: CallbackContext):
        print(update.callback_query.data)

    def run(self):
        print('polling')
        self.bot.run_polling()


if __name__ == "__main__":
    bot = MyBot('5671094663:AAGgo4DPNZlN-LdoFt9m_mD47BQb4QSzFTw')
    bot.run()
