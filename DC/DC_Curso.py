
def getCursos(cn):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "select id_curso, nombre from curso"
            if cursor.execute(sql) != 0:
                result = cursor.fetchall()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)


def getCursoDescription(cn, id_curso):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "SELECT descripcion,nombre,link FROM curso WHERE id_curso = " + str(id_curso)
            if cursor.execute(sql) != 0:
                result = cursor.fetchone()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)


def getCursoPreRequisitos(cn, id_curso):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "SELECT pre_requisito,nombre FROM curso WHERE id_curso = " + str(id_curso)+" and archivado = 0"
            if cursor.execute(sql) != 0:
                result = cursor.fetchone()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)

def getFechas(cn, id_curso):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "SELECT fecha_inscripcion, fecha_inicio,nombre FROM curso WHERE id_curso = " + str(id_curso)
            if cursor.execute(sql) != 0:
                result = cursor.fetchone()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)

def getProfesor(cn, id_curso):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "select nombre, email, twitter from docente inner join docente_curso curso on docente.id_docente = curso.id_docente_curso where  id_curso = " + str(id_curso)
            if cursor.execute(sql) != 0:
                result = cursor.fetchall()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)

def getDuracion(cn, id_curso):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "select nombre, esfuerzo_est,duracion from curso where id_curso = " + str(id_curso)
            if cursor.execute(sql) != 0:
                result = cursor.fetchone()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)

def getLink(cn, id_curso):
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "select nombre, link from curso where id_curso = " + str(id_curso)
            if cursor.execute(sql) != 0:
                result = cursor.fetchone()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)

def getContenido(cn, id_curso):
    try:
        with cn.cursor() as cursor:
            # Read all records
            sql = "select c.nombre, contenido from contenido inner join curso c on contenido.id_curso_cont = c.id_curso  where id_curso = " + str(id_curso)
            if cursor.execute(sql) != 0:
                result = cursor.fetchall()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)

def getCompetencias(cn, id_curso):
    try:
        with cn.cursor() as cursor:
            # Read all records
            sql = "select c.nombre, competencia from competencias inner join curso c on competencias.id_curso_comp = c.id_curso  where id_curso = " + str(id_curso)
            if cursor.execute(sql) != 0:
                result = cursor.fetchall()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)


def getRetos(cn, id_curso):
    try:
        with cn.cursor() as cursor:
            # Read all records
            sql = "select c.nombre, reto.descripcion, fecha_entrega from reto inner join curso c on reto.id_curso_reto = c.id_curso  where id_curso = " + str(id_curso)
            if cursor.execute(sql) != 0:
                result = cursor.fetchall()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)

