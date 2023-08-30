from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext, Application, ConversationHandler
from utils import get_address_info_graphql


WALLET = range(1)

dash_keys = [['Wallet']]
dash_markup = ReplyKeyboardMarkup(dash_keys, resize_keyboard=True)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Venom Bot", reply_markup=dash_markup)


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html("Paste the venom address starting with <i>\"0:\"</i> in the chat")


async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Enter the wallet address:', reply_markup=ReplyKeyboardRemove())
    return WALLET


# async def enter_wallet(update: Update, context: CallbackContext) -> int:
#     wallet_address = update.message.text
#     # Here you can process the wallet address and generate the information
#     info_text = f"Information for wallet address {wallet_address}:\n..."

#     await update.message.reply_text(info_text, reply_markup=dash_markup)


async def wallet_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('got a regex')
    address = update.message.text
    info = get_address_info_graphql(address)
    html = f"<b>Address:</b> <code>{info['address']}</code>\n\n<b>Balance:</b> <code>{info['balance']}</code> Venom"
    address_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("See on VenomScan",
                              web_app=WebAppInfo(url=f"https://testnet.venomscan.com/accounts/{info['address']}"))],
    ])
    await update.message.reply_text("Fetching the address info ...")
    await update.message.reply_html(html, reply_markup=address_markup)
    await update.message.reply_markup(dash_markup)
    return ConversationHandler.END


async def post_init(application: Application) -> None:
    """
    Post initialization hook for the bot.
    """
    commands = [
        BotCommand(command='start', description='starts the bot'),
        BotCommand(command='help', description='show the help you need'),
    ]
    await application.bot.set_my_name("Venom Bot")
    await application.bot.set_my_description("Your Bot interface to the venom blockchain")
    await application.bot.set_my_short_description("Your Venom Bot..")
    await application.bot.set_my_commands(commands)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(
        "5671094663:AAGgo4DPNZlN-LdoFt9m_mD47BQb4QSzFTw").post_init(post_init).build()
    # application = ApplicationBuilder().token(
    #     "6578677186:AAH1sUCAg4LPA1L29aujlIu7zrRB7cLFkkM").post_init(post_init).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(
            filters.Regex(r'(?i)wallet'), handle_wallet)],

        states={
            WALLET: [MessageHandler(
                filters.Regex(r'^0:[0-9a-fA-F]+$'), wallet_prompt)],
        },

        fallbacks=[]
    )
    # on different commands - answer in Telegram
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(CommandHandler("help", handle_help))
    application.add_handler(MessageHandler(
        filters.Regex(r'^0:[0-9a-fA-F]+$'), wallet_prompt))

    # Run the bot until the user presses Ctrl-C
    print("Polling..")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    return application.bot


if __name__ == "__main__":
    main()
