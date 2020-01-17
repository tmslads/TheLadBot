from time import sleep
import logging
import random as r

from telegram.ext import Updater
from telegram.ext import CommandHandler

import memes
import quotes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

MEMES_SENT = []

with open("token.txt", 'r') as file:
    bot_token = file.read()

updater = Updater(token=f'{bot_token}', use_context=True)
dispatcher = updater.dispatcher
lad_bot = updater.bot


def inspire(update, context):
    """Send a quote"""

    lad_bot.send_message(chat_id=update.effective_chat.id, text=f"{update.message.from_user.first_name} asked for some inspiration. you came to the right person broski.", disable_notification=True)
    sleep(1)
    lad_bot.send_message(chat_id=update.effective_chat.id, text=next(quote.QUOTES), disable_notification=True)


def send_meme(update, context):
    """Send a meme"""

    if update.effective_chat.type == 'private':
        name = 'you'
    else:
        name = update.message.from_user.first_name
    msg = f"{name} asked me for a meme. i have so many. here's a cute one\
    :\n(i'll delete it after a while cause seize the moment ye? bahaha)"
    msg_sent = lad_bot.send_message(chat_id=update.effective_chat.id, text=msg, disable_notification=True)
    sleep(1)
    title, url = memes.get_meme()[:2]
    photo_sent = lad_bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=title, disable_notification=True)
    MEMES_SENT.append((photo_sent, msg_sent, update.effective_chat.id, update.message.from_user.first_name))
    print(f"Meme sent for {update.message.from_user.first_name} {update.message.from_user.last_name} (username: {update.message.from_user.username}).")


def del_memes():
    """Delete the memes sent and edit the text message sent with them"""

    number = len(MEMES_SENT)
    for meme_sent in MEMES_SENT:  # Delete the photo sent
        meme_sent[0].delete()
    for meme_sent in MEMES_SENT:  # Edit the message sent
        edited_text = f"i sent a meme for {meme_sent[3]} but its deleted now. sent such a coolio meme and you missed it? lol better luck next time cow"
        lad_bot.edit_message_text(chat_id=meme_sent[2], message_id=meme_sent[1].message_id, text=edited_text)

    del MEMES_SENT[:]
    print(f"{number} meme(s) deleted.")


meme_handler = CommandHandler(command='meme', callback=send_meme)
dispatcher.add_handler(meme_handler)


updater.job_queue.run_repeating(del_memes, interval=120)  # will be called every 2 minutes
updater.start_polling()
