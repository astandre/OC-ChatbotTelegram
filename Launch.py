from decouple import config
import pymysql.cursors
from BL import BL_Curso, BL_FAQ
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

FAQ, FECHA, PRE, INFO = range(4)


def start(bot, update):
    reply_keyboard = [['Boy', 'Girl', 'Other']]
    user = update.message.from_user.username
    full_response = "Hola " + user + " soy OC-Chatbot, resolvere tus dudas sobre la plataforma Open Campus y sus cursos, puedes usar los comandos /informacion nombre del curso"
    update.message.reply_text(full_response,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def faq(bot, update):
    logger.debug("RAW-Mesage %s", update.message)
    user = update.message.from_user.username
    question = update.message.text
    logger.info(update.message)
    logger.info("FAQ [QUESTION] %s ", question)
    logger.info("FAQ [USER] %s ", user)
    resp = BL_FAQ.getRespuesta(connection, question)
    if resp != 0:
        size = 280 - (len(resp["link"]) + 16)
        full_response = resp["respuesta"][0:size] + "... " + resp["link"]
        update.message.reply_text(full_response)
    else:
        error = "No se ha encontrado " + question
        logger.error(error)
        update.message.reply_text(pregunta_no_encontrada)
    return FAQ


#
# def photo(bot, update):
#     user = update.message.from_user
#     photo_file = bot.get_file(update.message.photo[-1].file_id)
#     photo_file.download('user_photo.jpg')
#     logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
#     update.message.reply_text('Gorgeous! Now, send me your location please, '
#                               'or send /skip if you don\'t want to.')
#
#     return LOCATION
#
#
# def skip_photo(bot, update):
#     user = update.message.from_user
#     logger.info("User %s did not send a photo.", user.first_name)
#     update.message.reply_text('I bet you look great! Now, send me your location please, '
#                               'or send /skip.')
#
#     return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return INFO


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return INFO


def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def help(bot, update):
    logger.info("Se ha solicitado ayuda")
    update.message.reply_text('Los comandos soportados son: \n* /ayuda: muestra los comandos soportados '
                              '* /info *nombre del curso*: muestra informacion de un curso', parse_mode='Markdown')


def info(bot, update):
    logger.info("Raw-Message: %s", update.message)
    logger.info("INFO")
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/INFO":
        update.message.reply_text("Que curso te gustaria conocer?")
        logger.info("Ingrese el nombre del curso")
        return INFO
    else:
        if update.message.text[0:5].upper() == "/INFO":
            curso = update.message.text[update.message.entities[0]["length"] + 1:]
            logger.info("INFO [Curso] %s", curso)
            resp = BL_Curso.getCursoDescripcion(connection, curso)
            if resp != 0:
                size = 280 - (len(resp["nombre"]) + len(resp["link"]) + 20)
                full_response = resp["nombre"] + " " + resp["descripcion"][0:size] + "... " + \
                                resp["link"]
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
            else:
                error_curso = curso_no_encontrado + "'" + curso + "'" + curso_no_econtrado2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)
        else:
            curso = update.message.text
            if len(curso) > 6:
                logger.info("Raw-Message: %s ", update.message)
                logger.info("INFO [Curso] %s", curso)
                resp = BL_Curso.getCursoDescripcion(connection, curso)
                if resp != 0:
                    size = 280 - (len(resp["nombre"]) + len(resp["link"]) + 20)
                    full_response = resp["nombre"] + " " + resp["descripcion"][0:size] + "... " + \
                                    resp["link"]
                    update.message.reply_text(full_response)
                    logger.info("RESP: %s", full_response)
                else:
                    error_curso = curso_no_encontrado + "'" + curso + "'" + curso_no_econtrado2
                    logger.info("ERROR %s", error_curso)
                    update.message.reply_text(error_curso)


def prerequisitos(bot, update):
    logger.info("Raw-Message: %s", update.message)
    logger.info("INFO")
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/PRE":
        update.message.reply_text("Que curso te gustaria conocer?")
        logger.info("Ingrese el nombre del curso")
        return PRE
    else:
        if update.message.text[0:4].upper() == "/PRE":
            curso = update.message.text[update.message.entities[0]["length"] + 1:]
            logger.info("INFO [Curso] %s", curso)
            resp = BL_Curso.getCursoPrerequisitos(connection, curso)
            if resp != 0:
                if resp["pre_requisito"] == "Ninguno":
                    full_response = "No es necesario ningun *PREREQUISITO* para el curso "
                else:
                    full_response = "Los *PREREQUISITOS* para el curso " + resp["nombre"] + " son: " + resp[
                        "pre_requisito"]
                update.message.reply_text(full_response, parse_mode='Markdown')
                logger.info("RESP: %s", full_response)
            else:
                error_curso = curso_no_encontrado + "'" + curso + "'" + curso_no_econtrado2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)
        else:
            curso = update.message.text
            if len(curso) > 6:
                logger.info("Raw-Message: %s ", update.message)
                logger.info("INFO [Curso] %s", curso)
                resp = BL_Curso.getCursoPrerequisitos(connection, curso)
                if resp != 0:
                    if resp["pre_requisito"] == "Ninguno":
                        full_response = "No es necesario ningun *PREREQUISITO* para el curso "
                    else:
                        full_response = "Los *PREREQUISITO* para el curso " + resp["nombre"] + " son: " + resp[
                            "pre_requisito"]
                    update.message.reply_text(full_response, parse_mode='Markdown')
                    logger.info("RESP: %s", full_response)
                else:
                    error_curso = curso_no_encontrado + "'" + curso + "'" + curso_no_econtrado2
                    logger.info("ERROR %s", error_curso)
                    update.message.reply_text(error_curso)

def fechas(bot, update):
    logger.info("Raw-Message: %s", update.message)
    logger.info("INFO")
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/FECHAS":
        update.message.reply_text("Que curso te gustaria conocer?")
        logger.info("Ingrese el nombre del curso")
        return PRE
    else:
        if update.message.text[0:7].upper() == "/FECHAS":
            curso = update.message.text[update.message.entities[0]["length"] + 1:]
            logger.info("INFO [Curso] %s", curso)
            resp = BL_Curso.getFechas(connection, curso)
            if resp != 0:
                full_response = "La inscripcion al curso " + resp["nombre"] + " comienza el dia " + str(
                    resp["fecha_inscripcion"].strftime(
                        "%d-%m-%Y")) + " y el inicio de actividades es el dia " + str(
                    resp["fecha_inicio"].strftime("%d-%m-%Y"))
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
            else:
                error_curso = curso_no_encontrado + "'" + curso + "'" + curso_no_econtrado2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)
        else:
            curso = update.message.text
            if len(curso) > 7:
                logger.info("Raw-Message: %s ", update.message)
                logger.info("INFO [Curso] %s", curso)
                resp = BL_Curso.getFechas(connection, curso)
                if resp != 0:
                    full_response = "La inscripcion al curso " + resp["nombre"] + " comienza el dia " + str(
                        resp["fecha_inscripcion"].strftime(
                            "%d-%m-%Y")) + " y el inicio de actividades es el dia " + str(
                        resp["fecha_inicio"].strftime("%d-%m-%Y"))
                    update.message.reply_text(full_response)
                    logger.info("RESP: %s", full_response)
                else:
                    error_curso = curso_no_encontrado + "'" + curso + "'" + curso_no_econtrado2
                    logger.info("ERROR %s", error_curso)
                    update.message.reply_text(error_curso)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config('API_KEY'))

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('ayuda', help),
                      # CommandHandler('faq', faq),
                      # RegexHandler('(^/[a-zA-Z]\w)*', faq),
                      # TODO check this
                      # RegexHandler('(Ayuda|ayuda)', help),
                      CommandHandler('info', info),
                      CommandHandler('pre', prerequisitos),
                      CommandHandler('FECHAs', fechas)],

        states={
            # FAQ: [RegexHandler('([a-zA-Z]\w)*', faq)],

            # PHOTO: [MessageHandler(Filters.photo, photo),
            #         CommandHandler('skip', skip_photo)],

            PRE: [MessageHandler(Filters.text, fechas)],
            FECHA: [MessageHandler(Filters.text, prerequisitos)],

            INFO: [MessageHandler(Filters.text, info)]
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
    connection = pymysql.connect(host=config('HOST'),
                                 user=config('USER'),
                                 password=config('DB_PASS'),
                                 db=config('DB_NAME'),
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    curso_no_encontrado = "No he podido encontrar el curso "
    curso_no_econtrado2 = ", recuerda escribir bien el nombre del curso, consulta nuestra oferta de cursos en: http://opencampus.utpl.edu.ec/courses"
    pregunta_no_encontrada = "No he podido encontrar respuesta a tu pregunta, puedes revisar las preguntas frecuentes para más informacion http://opencampus.utpl.edu.ec/faq"
    respuesta_ayuda = "Puedes revisar la informacion de como usar el bot adelante: "
    print("\nStarting Telegram Chatbot t.me/OCCChatBot ....")
    main()
