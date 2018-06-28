from decouple import config
import pymysql.cursors
from BL import BL_Curso, BL_FAQ
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram import KeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

FAQ, FECHA, PRE, INFO, CURSO, MENU = range(6)


def start(bot, update):
    user = update.message.from_user.username
    full_response = "Hola " + user + " soy OC-Chatbot, resolvere tus dudas sobre la plataforma Open Campus y sus cursos"
    update.message.reply_text(full_response)
    menu(bot, update)


def menu(bot, update):
    logger.info("MENU")
    logger.debug("RAW-Mesage %s", update.message)
    reply_keyboard = [['/cursos - muestra los cursos actuales'],
                      # ['/info - muestra informacion de los cursos'], TODO make posible to display de function of the command
                      ['/info'],
                      ['/fechas'],
                      ['/pre'],
                      ['FAQ']]
    full_response = "Que te gustaria hacer?\n" +COMANDOS_DISPONIBLES
    update.message.reply_text(full_response,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def faq(bot, update):
    logger.info("FAQ")
    logger.debug("RAW-Mesage %s", update.message)
    user = update.message.from_user.username
    question = update.message.text
    if question[0:3].upper() == "FAQ":
        logger.info("si")
        update.message.reply_text("Ingresa tu pregunta")
        return FAQ
    else:
        logger.info("no")
        # if question[0] != "/":
        logger.info(update.message)
        logger.info("FAQ [QUESTION] %s ", question)
        logger.info("FAQ [USER] %s ", user)
        resp = BL_FAQ.getRespuesta(connection, question)
        if resp != 0:
            size = 280 - (len(resp["link"]) + 16)
            full_response = resp["respuesta"][0:size] + "... " + resp["link"]
            update.message.reply_text(full_response)
            logger.info("FAQ [RESP] %s ", full_response)
            menu(bot, update)
            return MENU
        else:
            error = "No se ha encontrado " + question
            logger.error(error)
            update.message.reply_text(PREGUNTA_NO_ENCONTRADA)



def cancel(bot, update):
    menu(bot, update)
    return ConversationHandler.END


def help(bot, update):
    logger.info("Se ha solicitado ayuda")
    update.message.reply_text(COMANDOS_DISPONIBLES, parse_mode='Markdown')


def info(bot, update):
    logger.info("INFO")
    logger.info("Raw-Message: %s", update.message)
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/INFO":
        logger.info("Ingrese el nombre del curso")
        displayCursosKeyboard(bot, update)
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
                # menu(bot, update)
                return MENU
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
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
                    # menu(bot, update)
                    return MENU
                else:
                    error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                    update.message.reply_text(error_curso)
                    logger.info("ERROR %s", error_curso)


def prerequisitos(bot, update):
    logger.info("PREREQUISITOS")
    logger.info("Raw-Message: %s", update.message)
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/PRE":
        logger.info("Ingrese el nombre del curso")
        displayCursosKeyboard(bot, update)
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
                # menu(bot, update)
                # return MENU
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
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
                    # menu(bot, update)
                    # return MENU
                else:
                    error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                    logger.info("ERROR %s", error_curso)
                    update.message.reply_text(error_curso)


def fechas(bot, update):
    logger.info("Raw-Message: %s", update.message)
    logger.info("INFO")
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/FECHAS":
        logger.info("Ingrese el nombre del curso")
        displayCursosKeyboard(bot, update)
        return FECHA
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
                # menu(bot, update)
                # return MENU
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
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
                    # menu(bot, update)
                    # return MENU
                else:
                    error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                    logger.info("ERROR %s", error_curso)
                    update.message.reply_text(error_curso)


def cursos(bot, update):
    resp = ""
    update.message.reply_text("Esta esta nuestra lista de cursos disponibles:")
    cursos_list = BL_Curso.getCursos(connection)
    if cursos_list != 0:
        for curso in cursos_list:
            resp = resp + "- *" + curso["nombre"] + "*\n "
        logger.info("[DEBUG] Desplegando lista de cursos")
        update.message.reply_text(resp, parse_mode='Markdown')
    else:
        logger.error("No se han encontrado cursos")



def displayCursosKeyboard(bot, update):
    cursos_list = BL_Curso.getCursos(connection)
    reply_keyboard = []
    for i in range(len(cursos_list)):
        row = []
        opcion = KeyboardButton(text=cursos_list[i]["nombre"])
        row.append(opcion)
        reply_keyboard.append(row)
    reply_keyboard.append(["/cancel"])
    full_response = "Que curso te gustaria conocer?"
    update.message.reply_text(text=full_response,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


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
                      CommandHandler('cursos', cursos),
                      # RegexHandler('^(FAQ|faq)$', faq),
                      CommandHandler('info', info),
                      CommandHandler('pre', prerequisitos),
                      CommandHandler('fechas', fechas),
                      # RegexHandler('(/{0}[a-zA-Z]\w)*', faq),
                      # TODO check this
                      CommandHandler('ayuda', help),
                      ],

        states={
            # FAQ: [RegexHandler('(/{0}[a-zA-Z]\w)*', faq)],
            # FAQ: [MessageHandler(Filters.text, faq),
            #       RegexHandler('([a-zA-Z]\w)*',faq)],
            # PHOTO: [MessageHandler(Filters.photo, photo),
            #         CommandHandler('skip', skip_photo)],
            PRE: [MessageHandler(Filters.text, prerequisitos),
                  CommandHandler('pre', prerequisitos)],
            FECHA: [MessageHandler(Filters.text, fechas),
                    CommandHandler('fechas', fechas)],
            INFO: [MessageHandler(Filters.text, info),
                   CommandHandler('info', info)],
            MENU: [MessageHandler(Filters.text, info),
                   CommandHandler('menu', menu)],
            # CURSO: [MessageHandler(Filters.text, aboutCurso),
            #         RegexHandler('([a-zA-Z]\w)*', aboutCurso)]
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
    COMANDOS_DISPONIBLES = "Los comandos soportados son: \n* /ayuda: muestra los comandos soportados\n " \
                           "- /cursos muestra todos los cursos disponibles\n"\
                           "- /info *nombre del curso*: muestra informacion de un curso\n" \
                           "- /fechas *nombre del curso*: muestra fechas importantes de un curso\n"\
                           "- /pre *nombre del curso*: muestra los prerequisitos de un curso"
    CURSO_NO_ENCONTRADO = "No he podido encontrar el curso "
    CURSO_NO_ECONTRADO2 = ", recuerda escribir bien el nombre del curso, consulta nuestra oferta de cursos en: http://opencampus.utpl.edu.ec/courses"
    PREGUNTA_NO_ENCONTRADA = "No he podido encontrar respuesta a tu pregunta, puedes revisar las preguntas frecuentes para más informacion http://opencampus.utpl.edu.ec/faq"
    RESPUESTA_AYUDA = "Puedes revisar la informacion de como usar el bot adelante: "
    test = ""
    print("\nStarting Telegram Chatbot t.me/OCCChatBot ....")
    main()
