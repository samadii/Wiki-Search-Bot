import logging

import requests
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
)
from telegram.ext.filters import Filters
from telegram.update import Update

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

import settings

updater = Updater(token=settings.TELEGRAM_TOKEN)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Assalamu alaykum va Rahmatullah! Welcome to the Wikipedia bot! In order to find something type /search and your request. For example /search Ibn Rushd"
    )


def search(update: Update, context: CallbackContext):
    args = context.args

    logging.info("checking args length")

    if len(args) == 0:
        update.message.reply_text(
            "Please type something. For example " "/search Elon Musk"
        )
    else:
        search_text = " ".join(args)
        logging.info("sending request to Wikipedia API")
        response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            {
                "action": "opensearch",
                "search": search_text,
                "limit": 1,
                "namespace": 0,
                "format": "json",
            },
        )

        logging.info("result from Wikipedia API")
        result = response.json()
        link = result[3]

        if len(link):
            update.message.reply_text("Links found: " + link[0])
        else:
            update.message.reply_text("Nothing Found")


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("search", search))
dispatcher.add_handler(MessageHandler(Filters.all, start))

updater.start_polling()
updater.idle()
