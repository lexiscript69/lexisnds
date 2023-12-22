import subprocess
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_TOKEN' with the actual API token from BotFather
TOKEN = '6549234833:AAEJgm7Epi51Lo_FpyRKkMb8hyieDAbuPE0'

def start(update, context):
    update.message.reply_text('Hello! I am your VPS bot.')

def status(update, context):
    update.message.reply_text('VPS is running smoothly.')

def start_attack(update, context):
    # Run the command on the VPS
    result = subprocess.run('service namso restart', shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        update.message.reply_text('Task done! Attack started.')
    else:
        update.message.reply_text(f'Failed to start attack. Error: {result.stderr}')

def custom_command(update, context):
    # Extract the custom command from the message
    custom_command = ' '.join(context.args) if context.args else None

    if custom_command:
        # Run the custom command on the VPS
        result = subprocess.run(custom_command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            update.message.reply_text('Task done! Custom command executed.')
        else:
            update.message.reply_text(f'Failed to execute custom command. Error: {result.stderr}')
    else:
        update.message.reply_text('Please specify a custom command after the command. E.g., /customcommand1 ls -l')

def echo(update, context):
    # Echo the user's message
    update.message.reply_text(f'You said: {update.message.text}')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("startattack", start_attack))
    dp.add_handler(CommandHandler("customcommand1", custom_command, pass_args=True))
    dp.add_handler(CommandHandler("customcommand2", custom_command, pass_args=True))

    # Add text message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
