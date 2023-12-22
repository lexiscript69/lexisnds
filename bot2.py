from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_TOKEN' with the actual API token from BotFather
TOKEN = '6549234833:AAEJgm7Epi51Lo_FpyRKkMb8hyieDAbuPE0'

# Dictionary to map service numbers to custom names and messages
SERVICE_DATA = {
    'ddosnamso': {'name': 'attack', 'message': 'namsogen is now underattack'},
    'stopnamsoddos': {'name': 'stop', 'message': 'ddos attack stopped'},
    'ddosrestart': {'name': 'Email Service', 'message': 'service restarted'}
}

def start(update, context):
    update.message.reply_text('Hello! I am your VPS bot.')

def status(update, context):
    update.message.reply_text('VPS is running smoothly.')

def restart_service(update, context):
    # Extract the service name and custom name from the command
    args = context.args
    if args:
        service_name = args[0]
        custom_name = args[1] if len(args) > 1 else None

        service_data = SERVICE_DATA.get(service_name)
        if service_data:
            custom_name_text = f' ({custom_name})' if custom_name else ''
            update.message.reply_text(f'Restarting {service_data["name"]}{custom_name_text}...')
            # Implement your logic to restart the corresponding service here
            # You might use subprocess or any other method depending on your setup
            # Placeholder: Simulating a restart
            update.message.reply_text(service_data['message'])
        else:
            update.message.reply_text('Invalid service name. Please use /ddosrestart, /stopnamsoddos, or /ddosnamso.')
    else:
        update.message.reply_text('Please specify a service name. E.g., /ddosrestart')

def echo(update, context):
    # Echo the user's message
    update.message.reply_text(f'You said: {update.message.text}')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

# Add command handlers
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("status", status))
dp.add_handler(CommandHandler("ddosnamso", lambda update, context: restart_service(update, context, ["namso", "start"]), pass_args=True))
dp.add_handler(CommandHandler("stopnamsoddos", lambda update, context: restart_service(update, context, ["namso", "stop"]), pass_args=True))
dp.add_handler(CommandHandler("ddosrestart", lambda update, context: restart_service(update, context, ["namso", "restart"]), pass_args=True))

    # Add text message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
