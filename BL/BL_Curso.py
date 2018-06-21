from DC import DC_Sinonimo, DC_Curso, DC_Tweets
import unicodedata


def getCursoDescripcion(connection, data):
    new_data = cleanData(data)
    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        resp = DC_Curso.getCursoDescription(connection, id_curso["id_curso_sin"])
        return resp
    else:
        return 0


def getCursoPrerequisitos(connection, data):
    new_data = cleanData(data)
    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        resp = DC_Curso.getCursoPreRequisitos(connection, id_curso["id_curso_sin"])
        return resp
    else:
        return 0


def getFechas(connection, data):
    new_data = cleanData(data)
    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        resp = DC_Curso.getFechas(connection, id_curso["id_curso_sin"])
        return resp
    else:
        return 0


def getProfesor(connection, data):
    new_data = cleanData(data)
    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        resp = DC_Curso.getProfesor(connection, id_curso["id_curso_sin"])
        return resp
    else:
        return 0


def getDuracion(connection, data):
    new_data = cleanData(data)
    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        resp = DC_Curso.getDuracion(connection, id_curso["id_curso_sin"])
        return resp
    else:
        return 0


def getLink(connection, data):
    new_data = cleanData(data)
    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        resp = DC_Curso.getLink(connection, id_curso["id_curso_sin"])
        return resp
    else:
        return 0


def getContenido(connection, data):
    new_data = cleanData(data)
    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        respuestas = DC_Curso.getContenido(connection, id_curso["id_curso_sin"])
        if respuestas != 0:
            for i in range(0, len(respuestas)):
                if respuestas[i]["contenido"][len(respuestas[i]["contenido"]) - 1] == ".":
                    respuestas[i]["contenido"] = respuestas[i]["contenido"][0:len(respuestas[i]["contenido"]) - 1]
            return respuestas
        else:
            return 0
    else:
        return 0


def getCompetencias(connection, data):
    new_data = cleanData(data)
    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        respuestas = DC_Curso.getCompetencias(connection, id_curso["id_curso_sin"])
        if respuestas != 0:
            for i in range(0, len(respuestas)):
                if respuestas[i]["competencia"][len(respuestas[i]["competencia"]) - 1] == ".":
                    respuestas[i]["competencia"] = respuestas[i]["competencia"][0:len(respuestas[i]["competencia"]) - 1]
            return respuestas
        else:
            return 0
    else:
        return 0


def getRetos(connection, data):
    new_data = cleanData(data)
    id_curso = DC_Sinonimo.getIdCurso(connection, new_data.upper())
    if id_curso != 0:
        retos = DC_Curso.getRetos(connection, id_curso["id_curso_sin"])
        return retos
    else:
        return 0


def cleanData(data):
    if data[0] == " ":
        data = data[1:len(data)]
    articles = ["el", "y", "la", "los", "tu", "las", "de", "para", "ellos", "de", "del", "una", "a", "tu"
                                                                                                     "EL", "Y", "LA",
                "LOS", "TU", "LAS", "DE", "PARA", "ELLOS", "DE", "DEL", "UNA", "A", "TU"]
    special = ["¿", "?", "!", "¡", "(", ")", ",", ".", ";", ":", "_", "{", "}", "[", "]", "+", "/", "*", "<",
               ">"]
    data_aux = ""
    for i in range(0, len(data)):
        if i + 1 <= len(data) - 1:
            if data[i] not in special:
                if data[i] == " ":
                    if data[i + 1] != " ":
                        data_aux = data_aux + data[i]
                else:
                    data_aux = data_aux + data[i]
    words = data_aux.split(" ")
    new_data = ""
    for word in words:
        if word not in articles:
            new_data = new_data + " " + word
    if new_data[0] == ' ':
        new_data = new_data[1:len(new_data)]
    if new_data[len(new_data) - 1] == ' ':
        new_data = new_data[0:len(new_data) - 1]
    return strip_accents(new_data)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')
