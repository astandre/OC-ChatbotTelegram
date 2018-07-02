
def insertTweet(cn, name, created_at, usuario, text, source, location,  input):
    """
    :param cn: Database connection
    :param data: data to be entered
    :return:
    """
    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = "INSERT INTO `inputs`( `nombre`, `created_at`, `usuario`, `texto`, `source`, `location`,`raw_input`) VALUES ('" + name + "','" + created_at + "','" + usuario + "','" + text + "','" + source + "','" + location + "'," + input + ")"
            cursor.execute(sql)
            cn.commit()
    except:
        print("error",Exception)

def getLastTweetId(cn):
    try:
        with cn.cursor() as cursor:
            sql = "SELECT id_input FROM inputs ORDER BY id_input DESC LIMIT 1"
            if cursor.execute(sql) != 0:
                result = cursor.fetchone()
                return result
            else:
                return 0
    except Exception:
        print("error", Exception)

def updateTweetResp(cn,id_tweet):

    try:
        with cn.cursor() as cursor:
            # Read a single record
            sql = " UPDATE `inputs`  SET `respuesta` = 1  WHERE  id_input =" + str(id_tweet)
            cursor.execute(sql)
            cn.commit()
    except:
        print("error")