from time import sleep
import logging
import random as r

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters

import memes
import quotes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

group_ids = {'12b': '-1001396726510', 'grade12': '-1001210862980', 'wait': '-1001427310423', 'testing' : '-1001248269460', 'pass' : '-375666484'}

MEMES_SENT = []

with open("token.txt", 'r') as file:
    bot_token = file.read()

updater = Updater(token=f'{bot_token}', use_context=True)
dispatcher = updater.dispatcher
lad_bot = updater.bot


def inspire(update, context):
    """Send a quote"""

    responses = ['Here\'s some good quotery for you',\
    'Here\'s a nice quote for you', 'Here you go',\
    'Here you are', 'This is a nice one',\
    'I like this one', 'This one really resonated with me',\
    'This one\'s cute', 'This is a cute one',\
    'Here\'s a cute quote', 'This one\'s pretty cool',\
    'Here\'s a nice quote for you', 'Here you go',\
    'Here you are', 'This is a nice quote',\
    'I like this quote', 'This quote really resonated with me',\
    'This quote\'s cute', 'This is a cute quote',\
    'Here\'s a cute quote', 'This is a cool quote',\
    'I think you\'ll like this one', 'I think you\'ll like this quote']

    quote = quotes.get_quote()
    lad_bot.send_message(chat_id=update.effective_chat.id, text=f"{r.choice(responses)}, {update.message.from_user.first_name}:", disable_notification=True)
    sleep(1)
    lad_bot.send_message(chat_id=update.effective_chat.id, text=f"<i><b>{quote}</b></i>", parse_mode='HTML', disable_notification=True)

    print(f"{update.message.from_user.first_name} {update.message.from_user.last_name} (username: {update.message.from_user.username}) was inspired.")

def send_meme(update, context):
    """Send a meme"""

    if update.effective_chat.type == 'private':
        name = 'you'
    else:
        name = update.message.from_user.first_name
    msg = f'meme for {name}'
    # msg = f"{name} asked me for a meme. i have so many. here's a cute one\
    # :\n(i'll delete it after a while cause seize the moment ye? bahaha)"
    msg_sent = lad_bot.send_message(chat_id=update.effective_chat.id, text=msg, disable_notification=True)
    sleep(1)
    title, url = memes.get_meme()[:2]
    photo_sent = lad_bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=title, disable_notification=True)
    MEMES_SENT.append((photo_sent, msg_sent, update.effective_chat.id, update.message.from_user.first_name))
    print(f"Meme sent for {update.message.from_user.first_name} {update.message.from_user.last_name} (username: {update.message.from_user.username}).")


def del_memes(context):
    """Delete the memes sent and edit the text message sent with them"""

    number = len(MEMES_SENT)
    for meme_sent in MEMES_SENT:  # Delete the photo sent
        meme_sent[0].delete()
    # for meme_sent in MEMES_SENT:  # Edit the message sent
        # edited_text = f"i sent a meme for {meme_sent[3]} but its deleted now. sent such a coolio meme and you missed it? lol better luck next time cow"
        # lad_bot.edit_message_text(chat_id=meme_sent[2], message_id=meme_sent[1].message_id, text=edited_text)

    del MEMES_SENT[:]
    print(f"{number} meme(s) deleted.")


def wadlord(update, context):
    """lad word = wad lord"""

    msg = update.message.text
    punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    msg = ''.join(c for c in msg if c not in punctuation)  # Strip punctuation from message
    msg = msg.split()
    if len(msg) == 2:
        if r.choice([0, 1]):
            print('wad lord in', update.effective_chat.title, f'({update.effective_chat.type})')
            waddened = msg[1][0] + msg[0][1:] + ' ' + msg[0][0] + msg[1][1:]  # the words exchange their first letters
            lad_bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text=waddened)


dispatcher.add_handler(MessageHandler(Filters.group & Filters.text & ~ Filters.update.edited_message, wadlord))
dispatcher.add_handler(CommandHandler(command='meme', callback=send_meme))
dispatcher.add_handler(CommandHandler(command='inspire', callback=inspire))

updater.job_queue.run_repeating(del_memes, interval=120)  # will be called every 2 minutes
updater.start_polling()
