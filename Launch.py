from decouple import config
import pymysql.cursors
from BL import BL_Curso, BL_FAQ, BL_Inputs
import json
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram import KeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

FAQ, FECHA, PRE, INFO, CURSO, MENU, DURACION, INSCRIPCION, DOCENTES, TEMAS, COMPETENCIAS, RETOS = range(12)


def start(bot, update):
    user = update.message.from_user.username
    full_response = "Hola " + user + " soy OC-Chatbot, resolvere tus dudas sobre la plataforma Open Campus y sus cursos"
    update.message.reply_text(full_response)
    menu(bot, update)


def menu(bot, update):
    logger.info("MENU")
    logger.debug("RAW-Mesage %s", update.message)
    reply_keyboard = [['/cursos'],
                      ['/info'],
                      ['/fechas'],
                      ['/prerequisitos'],
                      ['/duracion'],
                      ['/inscripcion'],
                      ['/docentes'],
                      ['/temas'],
                      ['/competencias'],
                      ['/retos'],
                      ['/faq']]
    full_response = "Que te gustaria hacer?\n" + COMANDOS_DISPONIBLES
    update.message.reply_text(full_response, parse_mode='Markdown',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def faq(bot, update):
    logger.info("FAQ")
    logger.info("Raw-Message: %s", update.message)
    user = update.message.from_user.username
    question = update.message.text
    logger.info(question[0:].upper())
    if question[0:4].upper() == "/FAQ":
        update.message.reply_text("Ingresa tu pregunta")
        return FAQ
    else:
        logger.info("FAQ [QUESTION] %s ", question)
        logger.info("FAQ [USER] %s ", user)
        full_name = update.message.chat.first_name + " " + update.message.chat.last_name
        date = update.message.date.strftime('%Y-%m-%d %H:%M:%S')
        full_message = '"' + str(update.message) + '"'
        if BL_Inputs.insertTweet(connection, full_name, date, user,
                                 update.message.text, "Telegram", "null", full_message) != 0:
            logger.info("Mensaje guardado en la Base de datos!")
        else:
            logger.info(" No se ha podido guardar el tweet")
        resp = BL_FAQ.getRespuesta(connection, question)
        if resp != 0:
            size = 280 - (len(resp["link"]) + 16)
            full_response = resp["respuesta"][0:size] + "... " + resp["link"]
            full_response = full_response + " Puedes usar /cancel para salir al menu."
            update.message.reply_text(full_response)
            logger.info("FAQ [RESP] %s ", full_response)
            # menu(bot, update)
            return FAQ
        else:
            error = "No se ha encontrado " + question + " Puedes usar /cancel para salir al menu."
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
                return INFO
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
                    return INFO
                else:
                    error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                    update.message.reply_text(error_curso)
                    logger.info("ERROR %s", error_curso)


def prerequisitos(bot, update):
    logger.info("PREREQUISITOS")
    logger.info("Raw-Message: %s", update.message)
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/PREREQUISITOS":
        logger.info("Ingrese el nombre del curso")
        displayCursosKeyboard(bot, update)
        return PRE
    else:
        if update.message.text[0:13].upper() == "/PREREQUISITOS":
            curso = update.message.text[update.message.entities[0]["length"] + 1:]
            logger.info("PREREQUISITOS [Curso] %s", curso)
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
                return PRE
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)
        else:
            curso = update.message.text
            logger.info("Raw-Message: %s ", update.message)
            logger.info("PREREQUISITOS [Curso] %s", curso)
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
                return PRE
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)


def fechas(bot, update):
    logger.info("Raw-Message: %s", update.message)
    logger.info("FECHAS")
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/FECHAS":
        logger.info("Ingrese el nombre del curso")
        displayCursosKeyboard(bot, update)
        return FECHA
    else:
        if update.message.text[0:7].upper() == "/FECHAS":
            curso = update.message.text[update.message.entities[0]["length"] + 1:]
            logger.info("FECHAS [Curso] %s", curso)
            resp = BL_Curso.getFechas(connection, curso)
            if resp != 0:
                full_response = "La inscripcion al curso " + resp["nombre"] + " comienza el dia " + str(
                    resp["fecha_inscripcion"].strftime(
                        "%d-%m-%Y")) + " y el inicio de actividades es el dia " + str(
                    resp["fecha_inicio"].strftime("%d-%m-%Y"))
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                # menu(bot, update)
                return FECHA
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)
        else:
            curso = update.message.text
            logger.info("Raw-Message: %s ", update.message)
            logger.info("FECHAS [Curso] %s", curso)
            resp = BL_Curso.getFechas(connection, curso)
            if resp != 0:
                full_response = "La inscripcion al curso " + resp["nombre"] + " comienza el dia " + str(
                    resp["fecha_inscripcion"].strftime(
                        "%d-%m-%Y")) + " y el inicio de actividades es el dia " + str(
                    resp["fecha_inicio"].strftime("%d-%m-%Y"))
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                # menu(bot, update)
                return FECHA
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)


def duracion(bot, update):
    logger.info("DURACION")
    logger.info("Raw-Message: %s", update.message)
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/DURACION":
        logger.info("Ingrese el nombre del curso")
        displayCursosKeyboard(bot, update)
        return DURACION
    else:
        if update.message.text[0:8].upper() == "/DURACION":
            curso = update.message.text[update.message.entities[0]["length"] + 1:]
            logger.info("DURACION [Curso] %s", curso)
            resp = BL_Curso.getDuracion(connection, curso)
            if resp != 0:
                full_response = "El curso " + resp["nombre"] + " tiene una #DURACION de " + str(
                    resp["duracion"]) + " semanas, con un esfuerzo estimado de " + str(
                    resp["esfuerzo_est"]) + " horas por semana"
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                # menu(bot, update)
                return DURACION
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)
        else:
            curso = update.message.text
            logger.info("Raw-Message: %s ", update.message)
            logger.info("DURACION [Curso] %s", curso)
            resp = BL_Curso.getDuracion(connection, curso)
            if resp != 0:
                full_response = "El curso " + resp["nombre"] + " tiene una #DURACION de " + str(
                    resp["duracion"]) + " semanas, con un esfuerzo estimado de " + str(
                    resp["esfuerzo_est"]) + " horas por semana"
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                # menu(bot, update)
                return DURACION
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                update.message.reply_text(error_curso)
                logger.info("ERROR %s", error_curso)


def inscripcion(bot, update):
    logger.info("INSCRIPCION")
    logger.info("Raw-Message: %s", update.message)
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/INSCRIPCION":
        logger.info("Ingrese el nombre del curso")
        displayCursosKeyboard(bot, update)
        return INSCRIPCION
    else:
        if update.message.text[0:11].upper() == "/INSCRIPCION":
            curso = update.message.text[update.message.entities[0]["length"] + 1:]
            logger.info("INSCRIPCION [Curso] %s", curso)
            resp = BL_Curso.getLink(connection, curso)
            if resp != 0:
                full_response = "Puedes inscribirte al curso " + resp["nombre"] + " en el siguiente enlace: " + \
                                resp["link"]
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                # menu(bot, update)
                return INSCRIPCION
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)
        else:
            curso = update.message.text
            logger.info("Raw-Message: %s ", update.message)
            logger.info("INSCRIPCION [Curso] %s", curso)
            resp = BL_Curso.getLink(connection, curso)
            if resp != 0:
                full_response = "Puedes inscribirte al curso " + resp["nombre"] + " en el siguiente enlace: " + \
                                resp["link"]
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                # menu(bot, update)
                return INSCRIPCION
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                update.message.reply_text(error_curso)
                logger.info("ERROR %s", error_curso)


def docentes(bot, update):
    logger.info("DOCENTES")
    logger.info("Raw-Message: %s", update.message)
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/DOCENTES":
        logger.info("Ingrese el nombre del curso")
        displayCursosKeyboard(bot, update)
        return DOCENTES
    else:
        if update.message.text[0:8].upper() == "/DOCENTES":
            curso = update.message.text[update.message.entities[0]["length"] + 1:]
            logger.info("DOCENTES [Curso] %s", curso)
            docentes = BL_Curso.getProfesor(connection, curso)
            if docentes != 0:
                if len(docentes) >= 2:
                    full_response = "Los docentes encargados son "
                    for docente in docentes:
                        full_response = full_response + docente["nombre"] + " (" + docente["email"] + ") "
                else:
                    if len(docentes[0]["twitter"]) > 0:
                        full_response = "El docente encargado es " + docentes[0]["nombre"] + " (" + docentes[0][
                            "email"] + ") " + docentes[0]["twitter"]
                    else:
                        full_response = "El docente encargado es " + docentes[0]["nombre"] + " (" + docentes[0][
                            "email"] + ")"
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                # menu(bot, update)
                return DOCENTES
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)
        else:
            curso = update.message.text
            logger.info("Raw-Message: %s ", update.message)
            logger.info("DOCENTES [Curso] %s", curso)
            docentes = BL_Curso.getProfesor(connection, curso)
            if docentes != 0:
                if len(docentes) >= 2:
                    full_response = "Los docentes encargados son "
                    for docente in docentes:
                        full_response = full_response + docente["nombre"] + " (" + docente["email"] + ") "
                else:
                    if len(docentes[0]["twitter"]) > 0:
                        full_response = "El docente encargado es " + docentes[0]["nombre"] + " (" + docentes[0][
                            "email"] + ") " + docentes[0]["twitter"]
                    else:
                        full_response = "El docente encargado es " + docentes[0]["nombre"] + " (" + docentes[0][
                            "email"] + ")"
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                # menu(bot, update)
                return DOCENTES
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                update.message.reply_text(error_curso)
                logger.info("ERROR %s", error_curso)


def temas(bot, update):
    logger.info("TEMAS")
    logger.info("Raw-Message: %s", update.message)
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/TEMAS":
        logger.info("Ingrese el nombre del curso")
        displayCursosKeyboard(bot, update)
        return TEMAS
    else:
        if update.message.text[0:5].upper() == "/TEMAS":
            curso = update.message.text[update.message.entities[0]["length"] + 1:]
            logger.info("TEMAS [Curso] %s", curso)
            contenidos = BL_Curso.getContenido(connection, curso)
            if contenidos != 0:
                full_response = "Los contenidos del curso " + contenidos[0]["nombre"] + " son "
                for i in range(0, len(contenidos)):
                    if i + 1 == len(contenidos):
                        full_response = full_response + contenidos[i]["contenido"]
                    else:
                        full_response = full_response + contenidos[i]["contenido"] + ", "
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                # menu(bot, update)
                return TEMAS
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)
        else:
            curso = update.message.text
            logger.info("Raw-Message: %s ", update.message)
            logger.info("TEMAS [Curso] %s", curso)
            contenidos = BL_Curso.getContenido(connection, curso)
            if contenidos != 0:
                full_response = "Los contenidos del curso " + contenidos[0]["nombre"] + " son "
                for i in range(0, len(contenidos)):
                    if i + 1 == len(contenidos):
                        full_response = full_response + contenidos[i]["contenido"]
                    else:
                        full_response = full_response + contenidos[i]["contenido"] + ", "
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                # menu(bot, update)
                return TEMAS
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                update.message.reply_text(error_curso)
                logger.info("ERROR %s", error_curso)


def competencias(bot, update):
    logger.info("COMPETENCIAS")
    logger.info("Raw-Message: %s", update.message)
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/COMPETENCIAS":
        logger.info("Ingrese el nombre del curso")
        displayCursosKeyboard(bot, update)
        return COMPETENCIAS
    else:
        if update.message.text[0:12].upper() == "/COMPETENCIAS":
            curso = update.message.text[update.message.entities[0]["length"] + 1:]
            logger.info("COMPETENCIAS [Curso] %s", curso)
            competencias = BL_Curso.getCompetencias(connection, curso)
            if competencias != 0:
                full_response = "Las competencias a obtener del curso: " + competencias[0]["nombre"] + " son: "
                for i in range(0, len(competencias)):
                    if i + 1 == len(competencias):
                        full_response = full_response + competencias[i]["competencia"]
                    else:
                        full_response = full_response + competencias[i]["competencia"] + ", "
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                return COMPETENCIAS
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)
        else:
            curso = update.message.text
            logger.info("Raw-Message: %s ", update.message)
            logger.info("COMPETENCIAS [Curso] %s", curso)
            competencias = BL_Curso.getCompetencias(connection, curso)
            if competencias != 0:
                full_response = "Las competencias a obtener del curso: " + competencias[0]["nombre"] + " son: "
                for i in range(0, len(competencias)):
                    if i + 1 == len(competencias):
                        full_response = full_response + competencias[i]["competencia"]
                    else:
                        full_response = full_response + competencias[i]["competencia"] + ", "
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                return COMPETENCIAS
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                update.message.reply_text(error_curso)
                logger.info("ERROR %s", error_curso)


def retos(bot, update):
    logger.info("RETOS")
    logger.info("Raw-Message: %s", update.message)
    logger.info(update.message.text.upper())
    if update.message.text.upper() == "/RETOS":
        logger.info("Ingrese el nombre del curso")
        displayCursosKeyboard(bot, update)
        return RETOS
    else:
        if update.message.text[0:5].upper() == "/RETOS":
            curso = update.message.text[update.message.entities[0]["length"] + 1:]
            logger.info("RETOS [Curso] %s", curso)
            resp = BL_Curso.getRetos(connection, curso)
            if resp != 0:
                if len(resp) >= 2:
                    full_response = "Los retos de " + resp[0]["nombre"] + " son "
                else:
                    full_response = "El reto de " + resp[0]["nombre"] + " es "
                for i in range(0, len(resp)):
                    if i + 1 == len(resp):
                        full_response = full_response + resp[i]["descripcion"] + " (" + resp[i][
                            "fecha_entrega"].strftime("%d-%m-%Y") + ")"
                    else:
                        full_response = full_response + resp[i]["descripcion"] + " (" + resp[i][
                            "fecha_entrega"].strftime("%d-%m-%Y") + ") , "
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                return RETOS
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                logger.info("ERROR %s", error_curso)
                update.message.reply_text(error_curso)
        else:
            curso = update.message.text
            logger.info("Raw-Message: %s ", update.message)
            logger.info("RETOS [Curso] %s", curso)
            resp = BL_Curso.getRetos(connection, curso)
            if resp != 0:
                if len(resp) >= 2:
                    full_response = "Los retos de " + resp[0]["nombre"] + " son "
                else:
                    full_response = "El reto de " + resp[0]["nombre"] + " es "
                for i in range(0, len(resp)):
                    if i + 1 == len(resp):
                        full_response = full_response + resp[i]["descripcion"] + " (" + resp[i][
                            "fecha_entrega"].strftime("%d-%m-%Y") + ")"
                    else:
                        full_response = full_response + resp[i]["descripcion"] + " (" + resp[i][
                            "fecha_entrega"].strftime("%d-%m-%Y") + ") , "
                update.message.reply_text(full_response)
                logger.info("RESP: %s", full_response)
                return RETOS
            else:
                error_curso = CURSO_NO_ENCONTRADO + "'" + curso + "'" + CURSO_NO_ECONTRADO2
                update.message.reply_text(error_curso)
                logger.info("ERROR %s", error_curso)


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
                      CommandHandler('faq', faq),
                      CommandHandler('info', info),
                      CommandHandler('prerequisitos', prerequisitos),
                      CommandHandler('fechas', fechas),
                      CommandHandler('duracion', duracion),
                      CommandHandler('inscripcion', inscripcion),
                      CommandHandler('docentes', docentes),
                      CommandHandler('temas', temas),
                      CommandHandler('competencias', competencias),
                      CommandHandler('retos', retos),
                      # RegexHandler('(/{0}[a-zA-Z]\w)*', faq),
                      # TODO check this
                      CommandHandler('ayuda', help),
                      ],

        states={
            # FAQ: [RegexHandler('(/{0}[a-zA-Z]\w)*', faq)],
            FAQ: [MessageHandler(Filters.text, faq),
                  CommandHandler('faq', faq)],
            # PHOTO: [MessageHandler(Filters.photo, photo),
            #         CommandHandler('skip', skip_photo)],
            PRE: [MessageHandler(Filters.text, prerequisitos),
                  CommandHandler('prerequisitos', prerequisitos)],
            FECHA: [MessageHandler(Filters.text, fechas),
                    CommandHandler('fechas', fechas)],
            DURACION: [MessageHandler(Filters.text, duracion),
                       CommandHandler('duracion', duracion)],
            DOCENTES: [MessageHandler(Filters.text, docentes),
                       CommandHandler('docentes', docentes)],
            TEMAS: [MessageHandler(Filters.text, temas),
                    CommandHandler('temas', temas)],
            INFO: [MessageHandler(Filters.text, info),
                   CommandHandler('info', info)],
            RETOS: [MessageHandler(Filters.text, retos),
                    CommandHandler('retos', retos)],
            COMPETENCIAS: [MessageHandler(Filters.text, competencias),
                           CommandHandler('competencias', competencias)],
            INSCRIPCION: [MessageHandler(Filters.text, inscripcion),
                          CommandHandler('inscripcion', inscripcion)],
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
    COMANDOS_DISPONIBLES = "Los comandos soportados son: \n" \
                           "- /ayuda: muestra los comandos soportados\n " \
                           "- /cursos muestra todos los cursos disponibles\n" \
                           "- /info *nombre del curso*: muestra informacion de un curso\n" \
                           "- /fechas *nombre del curso*: muestra fechas importantes de un curso\n" \
                           "- /pre *nombre del curso*: muestra los prerequisitos de un curso \n" \
                           "- /duracion *nombre del curso*: muestra la duracion del curso \n" \
                           "- /inscripcion *nombre del curso*: muestra donde me puedo inscribir al curso \n" \
                           "- /docentes *nombre del curso*: muestra informacion de el/los docentes encargados del curso \n" \
                           "- /temas *nombre del curso*: muestra los temas correspondientes al curso \n" \
                           "- /competencias *nombre del curso*: muestra las competencias a obtener del curso \n" \
                           "- /retos *nombre del curso*: muestra los retos del curso \n" \
                           "- /faq: pregunta sobre la plataforma open campus"
    CURSO_NO_ENCONTRADO = "No he podido encontrar el curso "
    CURSO_NO_ECONTRADO2 = ", recuerda escribir bien el nombre del curso, consulta nuestra oferta de cursos en: http://opencampus.utpl.edu.ec/courses"
    PREGUNTA_NO_ENCONTRADA = "No he podido encontrar respuesta a tu pregunta, puedes revisar las preguntas frecuentes para más informacion http://opencampus.utpl.edu.ec/faq"
    RESPUESTA_AYUDA = "Puedes revisar la informacion de como usar el bot adelante: "
    test = ""
    print("\nStarting Telegram Chatbot t.me/OCCChatBot ....")
    main()
