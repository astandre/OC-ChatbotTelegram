
def getIdCurso(cn, name):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "SELECT id_curso_sin FROM sinonimos inner join curso c on sinonimos.id_curso_sin = c.id_curso WHERE sinonimo LIKE '%" + name + "%'  and c.archivado = 0"
            if cursor.execute(sql) != 0:
                result = cursor.fetchone()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)