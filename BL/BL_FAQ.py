from DC import DC_FAQ, DC_Tweets
import unicodedata


def getRespuesta(connection, data):
    resp = DC_FAQ.getRespuesta(connection, cleanData(data))
    if resp != 0:
        return resp
    else:
        return 0


def cleanData(data):
    special = ["¿", "?", "!", "¡", "(", ")", ",", ".", ";", ":", "-", "-", "{", "}", "[", "]", "+", "-", "/", "*", "<",
               ">"]
    data_aux = ""
    for i in range(0, len(data)):
        if data[i] not in special:
            if i + 1 <= len(data) - 1:
                if data[i] == " ":
                    if data[i + 1] != " ":
                        data_aux = data_aux + data[i]
                else:
                    data_aux = data_aux + data[i]
    words = data_aux.split(" ")
    new_data = ""
    for word in words:
        new_data = new_data + " " + word
    if new_data[0] == ' ':
        new_data = new_data[1:len(new_data)]
    if new_data[len(new_data) - 1] == ' ':
        new_data = new_data[0:len(new_data) - 1]
    return strip_accents(new_data)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')
