import logging

from telegram import Update
from telegram.ext import CallbackContext


def add_user_record(update: Update, context: CallbackContext) -> None:
    full_name = update.effective_user.full_name
    username = update.effective_user.username

    if 'user' not in context.user_data:
        context.user_data['user'] = {'Full name': full_name, 'Username': username}
        logging.info(f"User data added for {full_name}")

    else:
        if context.user_data['user']['Full name'] != full_name or context.user_data['user']['Username'] != username:

            context.user_data['user'] = {'Full name': full_name, 'Username': username}
            logging.info(f"User data updated for {full_name}")

    context.dispatcher.persistence.flush()
