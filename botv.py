from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_TOKEN' with the actual API token from BotFather
TOKEN = '6549234833:AAEJgm7Epi51Lo_FpyRKkMb8hyieDAbuPE0'

def start(update, context):
    update.message.reply_text('Hello! I am your VPS bot.')

def status(update, context):
    update.message.reply_text('VPS is running smoothly.')

def echo(update, context):
    # Echo the user's message
    update.message.reply_text(f'You said: {update.message.text}')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))

    # Add text message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
