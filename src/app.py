#!/usr/bin/env python
import ctypes
import yaml
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import sqlite3

from utils.handle_messages import chat_bot_response
from client import FORMAT, STOP_KEYWORD, Client
from threading import Thread


with open("env.yaml", "r") as env_file:
    try:
        ENV_VARIABLES = yaml.safe_load(env_file)
        TOKEN = ENV_VARIABLES["TOKEN"]
        print('Connecting to db...')
        DB_DIR = './src/data/data.db'
        open(DB_DIR, 'w').close()
        db_conn = sqlite3.connect(DB_DIR, check_same_thread=False)
        c = db_conn.cursor()
        c.execute(
            "CREATE TABLE clients (user_id TEXT, client INT)")
        print('Connected to db!')
    except Exception as e:
        print(e)
        exit(1)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle the user message."""
    user_id = update.message.from_user.id
    c.execute("SELECT * FROM clients WHERE user_id = ?", (user_id,))
    person = c.fetchone()

    if not person:
        update.message.reply_text(
            chat_bot_response(update.message.text)
        )
        return

    try:
        client_id = person[1]
        client = ctypes.cast(client_id, ctypes.py_object).value
        client.send_message(update.message.text)
    except Exception as e:
        print(e)


def receive_message(update: Update, client: Client) -> None:
    try:
        while True:
            message = client.receive_message()
            if message == STOP_KEYWORD:
                return
            if message:
                update.message.reply_text(
                    message
                )
    except Exception as e:
        print(e)


def chatroom(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    c.execute("SELECT * FROM clients WHERE user_id = ?", (user_id,))
    person = c.fetchone()

    if person is not None:
        update.message.reply_text(
            "You are already in a chatroom!"
        )
        return

    try:
        client = Client()
        # TODO: Store client in db based on the user_id
        c.execute('INSERT INTO clients VALUES (?, ?)',
                  (user_id, id(client)))
        db_conn.commit()
        update.message.reply_text(
            "Welcome to the chatroom!"
        )

        thread = Thread(target=receive_message, args=(update, client), daemon=True)
        thread.start()
    except Exception as e:
        print(e)


def leaveroom(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    c.execute("SELECT * FROM clients WHERE user_id = ?", (user_id,))
    person = c.fetchone()

    if not person:
        update.message.reply_text(
            "You are not in a chatroom!"
        )
        return

    try:
        client_id = person[1]
        client = ctypes.cast(client_id, ctypes.py_object).value
        c.execute("DELETE FROM clients WHERE user_id = ?", (user_id,))
        db_conn.commit()

        client.send_message(STOP_KEYWORD)

        update.message.reply_text(
            "You have left the chatroom!"
        )

    except Exception as e:
        print(e)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # /start - says hello
    dispatcher.add_handler(CommandHandler("start", start))

    # On every other message  - handle the message answering content about Elon Musk
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, handle_message))

    dispatcher.add_handler(CommandHandler("chatroom", chatroom))
    dispatcher.add_handler(CommandHandler("leaveroom", leaveroom))

    # Start the Bot
    updater.start_polling()

    # Run the bot until proccess is closed (Ctrl-C)
    updater.idle()


if __name__ == '__main__':
    main()
