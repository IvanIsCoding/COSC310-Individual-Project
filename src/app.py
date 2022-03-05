#!/usr/bin/env python

import yaml
from hashlib import sha256
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pymongo import MongoClient

from utils.handle_messages import chat_bot_response
from client import STOP_KEYWORD, Client
from threading import Thread

FORMAT = 'utf8'
is_in_groupchat = False
mongo_client = MongoClient()
db = mongo_client.get_database('chatroom')

with open("env.yaml", "r") as env_file:
    ENV_VARIABLES = yaml.safe_load(env_file)
    TOKEN = ENV_VARIABLES["TOKEN"]


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle the user message."""
    if not is_in_groupchat:
        update.message.reply_text(
            chat_bot_response(update.message.text)
        )
    else:
        username = update.message.chat.username
        client = db.clients.find_one({"username": username})["client"]
        client.send_message(update.message.text)


def receive_message(update: Update, client: Client) -> None:
    while True:
        message = client.receive_message()
        update.message.reply_text(
            message
        )


def chatroom(update: Update, context: CallbackContext) -> None:
    global is_in_groupchat
    if is_in_groupchat:
        update.message.reply_text(
            "You are already in a chatroom!"
        )
        return

    try:
        is_in_groupchat = True
        client = Client()
        # TODO: Store client in db based on the username
        db.clients.insert_one({
            "username": update.message.chat.username,
            "client": client
        })
        thread = Thread(target=receive_message, args=(update, client))
        thread.daemon = True
        thread.start()
    except Exception as e:
        print(e)


def leavechat(update: Update, context: CallbackContext) -> None:
    global is_in_groupchat
    STOP_KEYWORD = sha256("x".encode(FORMAT)).hexdigest()

    username = update.message.chat.username

    if not is_in_groupchat:
        update.message.reply_text(
            "You are not in a chatroom!"
        )
        return

    try:
        # TODO: Look up db for client and end connection
        client = db.clients.find_one({"username": username})["client"]
        client.send_message(STOP_KEYWORD)
        is_in_groupchat = False
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
    dispatcher.add_handler(CommandHandler("leaveroom", leavechat))

    # Start the Bot
    updater.start_polling()

    # Run the bot until proccess is closed (Ctrl-C)
    updater.idle()


if __name__ == '__main__':
    main()
