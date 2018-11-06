from services import *
import constants
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction)
from telegram import KeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHAT, MENU = range(2)


def start(bot, update):
    user = update.message.from_user.username
    full_response = "Hola " + user + " soy OC-Chatbot, resolvere tus dudas sobre la plataforma Open Campus y sus cursos"
    update.message.reply_text(full_response)
    menu(bot, update)


def menu(bot, update):
    logger.info("MENU")
    full_response = "¿Que te gustaria hacer?\nLos comandos soportados son: \n"
    full_response += COMANDOS_DISPONIBLES_FULL
    update.message.reply_text(full_response, parse_mode='Markdown',
                              reply_markup=ReplyKeyboardMarkup(COMANDOS_DISPONIBLES, one_time_keyboard=True))


def chat(bot, update):
    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    logger.info("Raw-Message: %s", update.message)
    print(update)
    user_name = update.message.from_user.username
    content = update.message.text
    name = update.message.from_user.first_name + " " + update.message.from_user.last_name
    id_account = update.message.chat_id
    data = {"user_name": user_name, "content": content, "name": name, "id_account": id_account}
    if len(update.message.entities) > 0:
        data.update({"command": {"begin": update.message.entities[0].offset, "end": update.message.entities[0].length}})
    resp = chat_with_system(data)
    if resp is not None:
        update.message.reply_text(resp["output"])
    else:
        logger.error("Error")
        update.message.reply_text(constants.ERROR)


def cancel(bot, update):
    menu(bot, update)
    return ConversationHandler.END


def help(bot, update):
    logger.info("Se ha solicitado ayuda")
    update.message.reply_text(COMANDOS_DISPONIBLES_FULL, parse_mode='Markdown')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config('API_KEY'))

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('menu', menu),
                      RegexHandler('.', chat),
                      # RegexHandler('\w', chat),
                      # CommandHandler('cursos', chat),
                      CommandHandler('ayuda', help),
                      ],

        states={
            CHAT: [MessageHandler(Filters.text, chat),
                   CommandHandler('cursos', chat)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    # Launching App
    file_open = open("welcome.txt", "r")
    for line in file_open:
        print(line, end="")
    file_open.close()
    connection = None
    commands = init_chatbot()
    if commands is None:
        logger.info("Error al inicializar el bot")
    else:
        COMANDOS_DISPONIBLES = commands["simple"]
        COMANDOS_DISPONIBLES_FULL = commands["full"]
        print("\nStarting Telegram Chatbot " + constants.TELEGRAM_CHANNEL)
        main()
