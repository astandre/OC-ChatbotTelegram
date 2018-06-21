def getRespuesta(cn, question):
    """

    :param cn: Database connection
    :param pregunta: question to be answered
    :return:
    """
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "select p.pregunta,r.link,r.respuesta  from preguntas p " \
                  "inner join respuesta r on r.id_resp_intent = p.id_preg_intent" \
                  " where UPPER(p.pregunta) like '%" + question + "%'"
            if cursor.execute(sql) != 0:
                result = cursor.fetchone()
                return result
            else:
                return 0
    except:
        print ("error")

