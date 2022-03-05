#!/usr/bin/env python
import ctypes
import yaml
from hashlib import sha256
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pymongo import MongoClient

from utils.handle_messages import chat_bot_response
from client import FORMAT, STOP_KEYWORD, Client
from threading import Thread


with open("env.yaml", "r") as env_file:
    try:
        ENV_VARIABLES = yaml.safe_load(env_file)
        TOKEN = ENV_VARIABLES["TOKEN"]
        DB_HOST = ENV_VARIABLES["DB_HOST"]
        DB_PORT = ENV_VARIABLES["DB_PORT"]
        print('Connecting to db...')
        mongo_client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = mongo_client['chatroom']
        db.Clients.delete_many({})
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
    username = update.message.chat.username
    person = db.Clients.find_one({"username": username})

    if person is None or person["is_in_groupchat"] is None or not person["is_in_groupchat"]:
        update.message.reply_text(
            chat_bot_response(update.message.text)
        )
        return
    try:
        username = update.message.chat.username
        client_id = db.Clients.find_one({"username": username})["client"]
        client = ctypes.cast(client_id, ctypes.py_object).value
        client.send_message(update.message.text)
    except Exception as e:
        print(e)


def receive_message(update: Update, client: Client) -> None:
    while True:
        message = client.receive_message()
        if message:
            update.message.reply_text(
                message
            )


def chatroom(update: Update, context: CallbackContext) -> None:
    username = update.message.chat.username
    person = db.Clients.find_one({"username": username})

    if person is not None and person["is_in_groupchat"] is not None and person["is_in_groupchat"] == True:
        update.message.reply_text(
            "You are already in a chatroom!"
        )
        return

    try:
        client = Client()
        # TODO: Store client in db based on the username
        db.Clients.insert_one({
            "username": update.message.chat.username,
            "client": id(client),
            "is_in_groupchat": True
        })
        thread = Thread(target=receive_message, args=(update, client))
        thread.daemon = True
        thread.start()
    except Exception as e:
        print(e)


def leavechat(update: Update, context: CallbackContext) -> None:
    username = update.message.chat.username
    is_in_groupchat = db.Clients.find_one({"username": username})[
        "is_in_groupchat"]

    if not is_in_groupchat:
        update.message.reply_text(
            "You are not in a chatroom!"
        )
        return

    try:
        # TODO: Look up db for client and end connection
        db.Clients.find_one_and_update({"username": username}, {
                                       '$set': {"is_in_groupchat": False}})
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
