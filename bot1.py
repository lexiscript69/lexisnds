import subprocess
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_TOKEN' with the actual API token from BotFather
TOKEN = '6549234833:AAEJgm7Epi51Lo_FpyRKkMb8hyieDAbuPE0'

def start(update, context):
    update.message.reply_text('Hello! I am your VPS bot.')

def status(update, context):
    update.message.reply_text('VPS is running smoothly.')

def run_command_and_reply(update, command, reply_message):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        update.message.reply_text(f'Task done! {reply_message}.')
    else:
        update.message.reply_text(f'Failed to perform the task. Error: {result.stderr}')

def start_attack(update, context):
    run_command_and_reply(update, 'service namso restart', 'Attack started')

def restart_attack(update, context):
    run_command_and_reply(update, 'service namso restart', 'Attack restarted')

def stop_attack(update, context):
    run_command_and_reply(update, 'service namso stop', 'Attack stopped')

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
    dp.add_handler(CommandHandler("restartattack", restart_attack))
    dp.add_handler(CommandHandler("stopattack", stop_attack))

    # Add text message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
