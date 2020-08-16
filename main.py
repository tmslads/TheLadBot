from time import sleep
import logging
import random as r

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters
import telegram.utils

import submission_fetcher
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

msgs = ["Here's a nice _ for you", "Here you go",
"Here you are", "This is a nice one",
"I like this one", "This one really resonated with me",
"This one's cute", "This is a cute one",
"Here's a cute _", "This one's pretty cool",
"Here's a nice _ for you", "Here you go",
"Here you are", "This is a nice _",
"I like this _", "This _ really resonated with me",
"This _'s cute", "This is a cute _",
"Here's a cute _", "This is a cool _",
"I think you'll like this one", "I think you'll like this _"]


def inspire(update, context):
    """Send a quote"""

    quote = quotes.get_quote()
    msg = f"{r.choice(msgs).replace('_', 'quote')}, {update.message.from_user.first_name}:"
    lad_bot.send_message(chat_id=update.effective_chat.id, text=msg, disable_notification=True)
    sleep(1)
    lad_bot.send_message(chat_id=update.effective_chat.id,
                         text=f"<i><b>{quote}</b></i>", parse_mode='HTML', disable_notification=True)

    print(f"Inspiration sent for {update.message.from_user.first_name} {update.message.from_user.last_name} "
    f"(username: {update.message.from_user.username}).")


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
    post = submission_fetcher.meme_fetcher.get_post()
    title, url = post.title, post.url
    photo_sent = lad_bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=title, disable_notification=True)
    MEMES_SENT.append((photo_sent, msg_sent, update.effective_chat.id, update.message.from_user.first_name))
    print(f"Meme sent for {update.message.from_user.first_name} "
    f"{update.message.from_user.last_name} "
    f"(username: {update.message.from_user.username}).")


def send_song(update, context):
    """Send a song"""

    if update.effective_chat.type != 'private':  # If not called in a private chat
        # link = telegram.utils.helpers.create_deep_linked_url('@jumpiecookiebot')
        link = "@jumpiecookiebot"
        lad_bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id,
        text=f"Please message me at {link} and I will send you songs there.")
        return

    song = submission_fetcher.song_fetcher.get_post()
    msg = r.choice(msgs).replace('_', 'song')+':\n'+song.title
    lad_bot.send_message(chat_id=update.effective_chat.id, text=msg)
    sleep(1)
    lad_bot.send_message(chat_id=update.effective_chat.id, text=song.url)
    print(f"Song sent for {update.message.from_user.first_name} "
    f"{update.message.from_user.last_name} (username: {update.message.from_user.username}).")


def send_joke(update, context):
    """Send a dad joke"""

    joke = submission_fetcher.joke_fetcher.get_post()
    msg = joke.title + '\n\n' + joke.selftext
    lad_bot.send_message(chat_id=update.effective_chat.id, text=msg)
    print(f"Joke sent for {update.message.from_user.first_name} "
    f"{update.message.from_user.last_name} (username: {update.message.from_user.username}).")


def send_deal(update, context):
    """Send a game deal"""

    deal = submission_fetcher.deal_fetcher.get_post()
    post_link = 'https://reddit.com' + deal.permalink
    store_link = deal.url
    if post_link == store_link:  # if post is a selfpost (url is same as permalink)
        store_link = 'N/A'
    lad_bot.send_message(chat_id=update.effective_chat.id, text=f"Game deal for {update.message.from_user.first_name}: ")
    title = deal.title
    store = title[1:title.find(']')]  # extract store name from title
    # msg = f"{title[title.find(']')+1:]}\nStore: {store}\nReddit post({post_link})\nStore page({store_link})"
    msg = f"{title[title.find(']')+2:]}\nStore: {store}\n<a href=\"{post_link}\">Reddit post</a>\n<a href=\"{store_link}\">Store page</a>"
    print(msg)
    lad_bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='HTML')
    print(f"Game deal sent for {update.message.from_user.first_name} "
    f"{update.message.from_user.last_name} (username: {update.message.from_user.username}).")


def del_memes(context):
    """Delete the memes sent and edit the text message sent with them"""

    for meme_sent in MEMES_SENT:
        meme_sent[0].delete()  # Delete the photo sent

    # for meme_sent in MEMES_SENT:  # Edit the message sent
        # edited_text = f"i sent a meme for {meme_sent[3]} but its deleted now. sent such a coolio meme and you missed it? lol better luck next time cow"
        # lad_bot.edit_message_text(chat_id=meme_sent[2], message_id=meme_sent[1].message_id, text=edited_text)

    if MEMES_SENT:
        print("Memes deleted.")
    MEMES_SENT.clear()


def wadlord(update, context):
    """lad word = wad lord"""

    msg = update.message.text
    punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    msg = ''.join(c for c in msg if c not in punctuation)  # Strip punctuation from message
    msg = msg.split()
    if len(msg) == 2:
        if r.choices([0, 1], weights=[0.9, 0.1], k=1)[0]:  # (Returns list with one element)
            print('wad lord in', update.effective_chat.title, f'({update.effective_chat.type})')
            waddened = msg[1][0] + msg[0][1:] + ' ' + msg[0][0] + msg[1][1:]  # the words exchange their first letters
            lad_bot.send_message(chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.message_id, text=f"{' '.join(msg)} more like {waddened}")


def thanks(update, context):
    """thank you"""

    if update.message.reply_to_message.from_user.id == lad_bot.id:
        lad_bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text="thank you")
        print(f"Thank you to {update.message.from_user.full_name} in {update.effective_chat.title}.")


dispatcher.add_handler(CommandHandler(command='joke', callback=send_joke))
dispatcher.add_handler(CommandHandler(command='meme', callback=send_meme))
dispatcher.add_handler(CommandHandler(command='song', callback=send_song))
dispatcher.add_handler(CommandHandler(command='inspire', callback=inspire))
dispatcher.add_handler(CommandHandler(command='deal', callback=send_deal))
dispatcher.add_handler(MessageHandler(Filters.group & Filters.text & ~ Filters.update.edited_message, wadlord), group=0)
dispatcher.add_handler(MessageHandler(Filters.reply, thanks), group=1)

# updater.job_queue.run_repeating(del_memes, interval=120)  # will be called every 2 minutes
updater.start_polling()
